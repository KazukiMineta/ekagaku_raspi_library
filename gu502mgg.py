### Basic Libraries for e-kagaku's RasPi Course ###
#------------------------------------------------------------------------------------------#
### File name	:	gu502mgg.py
### Version		:	ver.0.1
### Created by	:	e-kagaku Supporter, Kazuki Mineta

### Purpose		:	This file is a library containing functions useful for the gnss module (GU-502MGG-USB).
### Datasheet 	:	https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
#------------------------------------------------------------------------------------------#
# pip install pyserial

import serial

def open_port(port, baudrate=9600, timeout=1.0):
    """GNSS のシリアルポートを開く"""
    return serial.Serial(port=port, baudrate=baudrate, timeout=timeout)


def read_raw_nmea(ser):
    """生の NMEA 文を1行取得する（文字列）"""
    line = ser.readline()
    if not line:
        return None
    return line.decode(errors="ignore").strip()

def _checksum_ok(sentence):
    """NMEA チェックサム確認"""
    if not sentence.startswith("$") or "*" not in sentence:
        return False

    body, cks = sentence[1:].split("*", 1)
    calc = 0
    for ch in body:
        calc ^= ord(ch)

    try:
        given = int(cks[:2], 16)
    except ValueError:
        return False

    return calc == given


def _to_deg(raw, hemi):
    """ddmm.mmmm → 10進度"""
    if raw == "" or hemi == "":
        return None

    try:
        v = float(raw)
    except ValueError:
        return None

    deg = int(v // 100)
    minutes = v - deg * 100
    dec = deg + minutes / 60.0

    if hemi in ("S", "W"):
        dec = -dec

    return dec

def get_raw_data(ser):
    """
    生の NMEA 文を返す（GGA/RMC など区別なし）
    """
    return read_raw_nmea(ser)

def get_lat_lon(ser):
    """
    GGA または RMC から緯度・経度を取得して返す
    戻り値: (lat, lon) または (None, None)
    """
    while True:
        line = read_raw_nmea(ser)
        if line is None:
            return (None, None)

        if not _checksum_ok(line):
            continue

        parts = line.split(",")

        # GGA
        if "GGA" in parts[0]:
            lat = _to_deg(parts[2], parts[3])
            lon = _to_deg(parts[4], parts[5])
            return (lat, lon)

        # RMC
        if "RMC" in parts[0]:
            lat = _to_deg(parts[3], parts[4])
            lon = _to_deg(parts[5], parts[6])
            return (lat, lon)

def get_satellite_info(ser):
    """
    GGA 文から衛星数(num_sv) と HDOP を取得
    戻り値: (num_sv, hdop)
    """
    while True:
        line = read_raw_nmea(ser)
        if line is None:
            return (None, None)

        if not _checksum_ok(line):
            continue

        parts = line.split(",")

        if "GGA" in parts[0]:
            # 衛星数
            try:
                num_sv = int(parts[7])
            except:
                num_sv = None

            # HDOP
            try:
                hdop = float(parts[8])
            except:
                hdop = None

            return (num_sv, hdop)

#------------------------------------------------------------------------------------------#
### Update history:
# 2026/02/21    ver.0.1     Added gu502mgg.py
#------------------------------------------------------------------------------------------#