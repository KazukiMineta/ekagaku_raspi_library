### Basic Libraries for e-kagaku's RasPi Course ###
#------------------------------------------------------------------------------------------#
### File name	:	mfrc522.py
### Version		:	ver.0.1
### Created by	:	e-kagaku Supporter, Kazuki Mineta

### Purpose		:	
### Datasheet 	:	
#------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------#
### Update history:
# 2026/02/17	ver.0.1		Added mfrc522.py
#------------------------------------------------------------------------------------------#
import RPi.GPIO as GPIO
import spidev
import time

class MFRC522:
    # 一部レジスタ定義（最低限）
    CommandReg      = 0x01
    CommIEnReg      = 0x02
    DivIEnReg       = 0x03
    CommIrqReg      = 0x04
    ErrorReg        = 0x06
    Status2Reg      = 0x08
    FIFODataReg     = 0x09
    FIFOLevelReg    = 0x0A
    ControlReg      = 0x0C
    BitFramingReg   = 0x0D
    ModeReg         = 0x11
    TxControlReg    = 0x14

    PCD_IDLE        = 0x00
    PCD_AUTHENT     = 0x0E
    PCD_TRANSCEIVE  = 0x0C

    PICC_REQIDL     = 0x26
    PICC_ANTICOLL   = 0x93
    PICC_AUTH_KEYA  = 0x60
    PICC_WRITE      = 0xA0

    def __init__(self, rst=22, cs=0, spi_bus=0, spi_dev=0):
        self.RST = rst
        self.CS = cs

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RST, GPIO.OUT)
        GPIO.setup(self.CS, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_dev)
        self.spi.max_speed_hz = 1000000

        GPIO.output(self.RST, 1)
        self._init_mfrc522()

    def _write_reg(self, addr, val):
        GPIO.output(self.CS, 0)
        self.spi.xfer2([(addr << 1) & 0x7E, val])
        GPIO.output(self.CS, 1)

    def _read_reg(self, addr):
        GPIO.output(self.CS, 0)
        val = self.spi.xfer2([((addr << 1) & 0x7E) | 0x80, 0])[1]
        GPIO.output(self.CS, 1)
        return val

    def _set_bit_mask(self, reg, mask):
        val = self._read_reg(reg)
        self._write_reg(reg, val | mask)

    def _clear_bit_mask(self, reg, mask):
        val = self._read_reg(reg)
        self._write_reg(reg, val & (~mask))

    def _antenna_on(self):
        val = self._read_reg(self.TxControlReg)
        if ~(val & 0x03):
            self._set_bit_mask(self.TxControlReg, 0x03)

    def _init_mfrc522(self):
        self._write_reg(self.CommandReg, self.PCD_IDLE)
        self._write_reg(self.ModeReg, 0x3D)
        self._antenna_on()

    def _to_card(self, command, send_data):
        self._write_reg(self.CommandReg, self.PCD_IDLE)
        self._write_reg(self.FIFOLevelReg, 0x80)

        for d in send_data:
            self._write_reg(self.FIFODataReg, d)

        self._write_reg(self.CommandReg, command)
        if command == self.PCD_TRANSCEIVE:
            self._set_bit_mask(self.BitFramingReg, 0x80)

        i = 2000
        while True:
            n = self._read_reg(self.CommIrqReg)
            i -= 1
            if not (i != 0 and not (n & 0x01) and not (n & 0x30)):
                break

        self._clear_bit_mask(self.BitFramingReg, 0x80)

        if i == 0:
            return None, None

        if (self._read_reg(self.ErrorReg) & 0x1B) != 0:
            return None, None

        length = self._read_reg(self.FIFOLevelReg)
        res = []
        for _ in range(length):
            res.append(self._read_reg(self.FIFODataReg))

        return res, length

    def request(self):
        self._write_reg(self.BitFramingReg, 0x07)
        (res, _) = self._to_card(self.PCD_TRANSCEIVE, [self.PICC_REQIDL])
        return res

    def anticoll(self):
        ser_num = [self.PICC_ANTICOLL, 0x20]
        self._write_reg(self.BitFramingReg, 0x00)
        (res, length) = self._to_card(self.PCD_TRANSCEIVE, ser_num)
        if res and length >= 5:
            return res[:5]
        return None

    def read_uid(self):
        if self.request() is None:
            return None
        uid = self.anticoll()
        return uid

    # ------------------------------
    # 認証
    # ------------------------------
    def auth(self, block_addr, key=[0xFF]*6, uid=None):
        if uid is None:
            return False

        auth_cmd = [self.PICC_AUTH_KEYA, block_addr] + key + uid[:4]
        (res, _) = self._to_card(self.PCD_AUTHENT, auth_cmd)

        status = self._read_reg(self.Status2Reg)
        return (status & 0x08) != 0

    # ------------------------------
    # 書き込み
    # ------------------------------
    def write_block(self, block_addr, data16):
        if len(data16) != 16:
            raise ValueError("data16 must be 16 bytes")

        (res, _) = self._to_card(self.PCD_TRANSCEIVE, [self.PICC_WRITE, block_addr])
        if not res or (res[0] & 0x0F) != 0x0A:
            return False

        (res, _) = self._to_card(self.PCD_TRANSCEIVE, data16)
        if not res or (res[0] & 0x0F) != 0x0A:
            return False

        return True

    def cleanup(self):
        self.spi.close()
        GPIO.cleanup()