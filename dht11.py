### Basic Libraries for e-kagaku's RasPi Course ###
#------------------------------------------------------------------------------------------#
### File name	:	dht11.py
### Version		:	ver.0.1
### Created by	:	e-kagaku Supporter, Kazuki Mineta

### Purpose		:	This file is a library containing functions useful for the temperature/humidity sensor module (DHT11).
### Datasheet 	:	https://akizukidenshi.com/goodsaffix/DHT11_20180119.pdf
#------------------------------------------------------------------------------------------#
import time
import RPi.GPIO as GPIO

def _wait_for(pin, value, timeout=100):
    """ピンが指定の状態から変化するまで待つ（タイムアウト付き）"""
    count = 0
    while GPIO.input(pin) == value:
        count += 1
        if count > timeout:
            return False
    return True


def read(pin):
    """DHT11 の温度・湿度を読み取る（失敗時は None, None を返す）"""

    GPIO.setmode(GPIO.BCM)

    # Start signal
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.018)  # 18ms
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.00004)  # 40us

    # Input mode
    GPIO.setup(pin, GPIO.IN)

    # DHT11 response
    if not _wait_for(pin, GPIO.LOW):
        return None, None
    if not _wait_for(pin, GPIO.HIGH):
        return None, None

    # Read 40 bits
    data = []
    for i in range(40):
        if not _wait_for(pin, GPIO.LOW):
            return None, None

        start = time.time()
        if not _wait_for(pin, GPIO.HIGH):
            return None, None

        pulse = time.time() - start
        data.append(1 if pulse > 0.00005 else 0)

    # Convert bits → bytes
    bytes_ = [
        int("".join(str(bit) for bit in data[i:i+8]), 2)
        for i in range(0, 40, 8)
    ]

    humidity = bytes_[0]
    temperature = bytes_[2]
    checksum = bytes_[4]

    # Checksum
    if (bytes_[0] + bytes_[2]) & 0xFF != checksum:
        return None, None

    return humidity, temperature

#------------------------------------------------------------------------------------------#
### Update history:
# 2026/02/17	ver.0.2		Added dht11.py
#------------------------------------------------------------------------------------------#