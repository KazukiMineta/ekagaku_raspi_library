import spidev

class MCP3008:
    def __init__(self, bus=0, device=0, max_speed=1350000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed

    def read(self, ch):
        """
        Read MCP3008 channel (0-7)
        Returns 0-1023
        """
        if ch < 0 or ch > 7:
            raise ValueError("Channel must be 0-7")

        # MCP3008 command format:
        # Start bit(1), Single-ended(1), Channel(3)
        cmd = 0b11 << 6 | (ch & 0b111) << 3

        # Send 3 bytes: [cmd, 0, 0]
        r = self.spi.xfer2([cmd, 0, 0])

        # Combine result (10bit)
        value = ((r[1] & 0x0F) << 8) | r[2]
        return value

    def close(self):
        self.spi.close()

