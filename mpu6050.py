### Basic Libraries for e-kagaku's RasPi Course ###
#------------------------------------------------------------------------------------------#
### File name	:	mpu6050.py
### Version		:	ver.0.1
### Created by	:	e-kagaku Supporter, Kazuki Mineta

### Purpose		:	This file is a library containing functions useful for the 6-axis gyro sensor module (MPU6050).
### Datasheet 	:	
#------------------------------------------------------------------------------------------#
# mpu6050.py
import smbus
import time

# --- レジスタ定義 ---
MPU6050_ADDR = 0x68
PWR_MGMT_1   = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H  = 0x43

# スケール（デフォルト設定）
ACCEL_SCALE = 16384.0   # ±2g
GYRO_SCALE  = 131.0     # ±250deg/s

# --- 初期化 ---
def mpu_init(bus=1, addr=MPU6050_ADDR):
    global _bus, _addr
    _bus = smbus.SMBus(bus)
    _addr = addr

    # スリープ解除
    _bus.write_byte_data(_addr, PWR_MGMT_1, 0)
    time.sleep(0.1)

# --- 16bit の生データ読み取り ---
def read_raw(reg):
    high = _bus.read_byte_data(_addr, reg)
    low  = _bus.read_byte_data(_addr, reg + 1)
    value = (high << 8) | low

    # 負数処理（2の補数）
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

# --- 加速度（g） ---
def read_accel():
    ax = read_raw(ACCEL_XOUT_H)     / ACCEL_SCALE
    ay = read_raw(ACCEL_XOUT_H + 2) / ACCEL_SCALE
    az = read_raw(ACCEL_XOUT_H + 4) / ACCEL_SCALE
    return ax, ay, az

# --- 角速度（deg/s） ---
def read_gyro():
    gx = read_raw(GYRO_XOUT_H)     / GYRO_SCALE
    gy = read_raw(GYRO_XOUT_H + 2) / GYRO_SCALE
    gz = read_raw(GYRO_XOUT_H + 4) / GYRO_SCALE
    return gx, gy, gz

# --- まとめて取得 ---
def read_all():
    ax, ay, az = read_accel()
    gx, gy, gz = read_gyro()
    return {
        "accel": (ax, ay, az),
        "gyro":  (gx, gy, gz)
    }

#------------------------------------------------------------------------------------------#
### Update history:
# 2026/02/17	ver.0.2		Added mpu6050.py
#------------------------------------------------------------------------------------------#