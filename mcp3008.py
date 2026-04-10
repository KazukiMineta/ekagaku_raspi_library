import spidev

class MCP3008:
    def __init__(self, bus=0, device=0, max_speed=1350000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed

    def read(self, ch):
        """
        MCP3008 の単一エンド入力を読む（0〜7）
        戻り値：0〜1023
        """
        if not 0 <= ch <= 7:
            raise ValueError("Channel must be 0-7")

        # 正しい MCP3008 コマンド
        # [1, (8 + ch) << 4, 0]
        r = self.spi.xfer2([1, (8 + ch) << 4, 0])

        # 10bit データを合成
        value = ((r[1] & 3) << 8) | r[2]
        return value

    def close(self):
        self.spi.close()