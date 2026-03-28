### Basic Libraries for e-kagaku's RasPi Course ###
#------------------------------------------------------------------------------------------#
### File name	:	bm3280.py
### Version		:	ver.0.1
### Created by	:	e-kagaku Supporter, Kazuki Mineta

### Purpose		:	This file is a library containing functions useful for the temperature/humidity sensor module (bme280).
### Datasheet 	:	
#------------------------------------------------------------------------------------------#
import smbus
import time

# 補正係数を保持
CALIB = {}

# I2C バス
bus = smbus.SMBus(1)

def _read_u16_le(addr, i2c_addr):
    lsb = bus.read_byte_data(i2c_addr, addr)
    msb = bus.read_byte_data(i2c_addr, addr + 1)
    return (msb << 8) | lsb

def _read_s16_le(addr, i2c_addr):
    val = _read_u16_le(addr, i2c_addr)
    return val - 65536 if val > 32767 else val

def load_calibration(i2c_addr):
    global CALIB

    CALIB = {
        "T1": _read_u16_le(0x88, i2c_addr),
        "T2": _read_s16_le(0x8A, i2c_addr),
        "T3": _read_s16_le(0x8C, i2c_addr),

        "P1": _read_u16_le(0x8E, i2c_addr),
        "P2": _read_s16_le(0x90, i2c_addr),
        "P3": _read_s16_le(0x92, i2c_addr),
        "P4": _read_s16_le(0x94, i2c_addr),
        "P5": _read_s16_le(0x96, i2c_addr),
        "P6": _read_s16_le(0x98, i2c_addr),
        "P7": _read_s16_le(0x9A, i2c_addr),
        "P8": _read_s16_le(0x9C, i2c_addr),
        "P9": _read_s16_le(0x9E, i2c_addr),

        "H1": bus.read_byte_data(i2c_addr, 0xA1),
        "H2": _read_s16_le(0xE1, i2c_addr),
        "H3": bus.read_byte_data(i2c_addr, 0xE3),
    }

    e4 = bus.read_byte_data(i2c_addr, 0xE4)
    e5 = bus.read_byte_data(i2c_addr, 0xE5)
    e6 = bus.read_byte_data(i2c_addr, 0xE6)

    CALIB["H4"] = (e4 << 4) | (e5 & 0x0F)
    CALIB["H5"] = (e6 << 4) | (e5 >> 4)
    CALIB["H6"] = bus.read_byte_data(i2c_addr, 0xE7)

def init(i2c_addr=0x76):
    load_calibration(i2c_addr)
    bus.write_byte_data(i2c_addr, 0xF2, 0x01)  # 湿度 oversampling x1
    bus.write_byte_data(i2c_addr, 0xF4, 0x27)  # temp/press oversampling x1, normal mode
    bus.write_byte_data(i2c_addr, 0xF5, 0xA0)  # standby 1000ms
    time.sleep(0.2)

def read_temperature(i2c_addr=0x76):
    data = bus.read_i2c_block_data(i2c_addr, 0xFA, 3)
    raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)

    T1, T2, T3 = CALIB["T1"], CALIB["T2"], CALIB["T3"]

    var1 = (raw / 16384.0 - T1 / 1024.0) * T2
    var2 = ((raw / 131072.0 - T1 / 8192.0) ** 2) * T3
    t_fine = var1 + var2
    temp = t_fine / 5120.0

    return temp, t_fine

def read_pressure(i2c_addr=0x76):
    data = bus.read_i2c_block_data(i2c_addr, 0xF7, 3)
    raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)

    temp, t_fine = read_temperature(i2c_addr)

    p1 = CALIB["P1"]
    p2 = CALIB["P2"]
    p3 = CALIB["P3"]
    p4 = CALIB["P4"]
    p5 = CALIB["P5"]
    p6 = CALIB["P6"]
    p7 = CALIB["P7"]
    p8 = CALIB["P8"]
    p9 = CALIB["P9"]

    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * p6 / 32768.0
    var2 += var1 * p5 * 2.0
    var2 = var2 / 4.0 + p4 * 65536.0
    var1 = (p3 * var1 * var1 / 524288.0 + p2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * p1

    if var1 == 0:
        return None

    press = 1048576.0 - raw
    press = ((press - var2 / 4096.0) * 6250.0) / var1
    var1 = p9 * press * press / 2147483648.0
    var2 = press * p8 / 32768.0
    press = press + (var1 + var2 + p7) / 16.0

    return press / 100.0  # hPa

def read_humidity(i2c_addr=0x76):
    data = bus.read_i2c_block_data(i2c_addr, 0xFD, 2)
    raw = (data[0] << 8) | data[1]

    temp, t_fine = read_temperature(i2c_addr)

    h1 = CALIB["H1"]
    h2 = CALIB["H2"]
    h3 = CALIB["H3"]
    h4 = CALIB["H4"]
    h5 = CALIB["H5"]
    h6 = CALIB["H6"]

    hum = t_fine - 76800.0
    hum = (raw - (h4 * 64.0 + h5 / 16384.0 * hum)) * \
          (h2 / 65536.0 * (1.0 + h6 / 67108864.0 * hum *
          (1.0 + h3 / 67108864.0 * hum)))

    hum = hum * (1.0 - h1 * hum / 524288.0)

    return max(0.0, min(100.0, hum))

def calc_altitude(pressure, sea_level=1013.25):
    pass