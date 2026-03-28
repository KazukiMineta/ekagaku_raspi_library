from ekagaku_raspi_library import gu502mgg as gnss
import time

ser = gnss.open_port("/dev/ttyUSB0")

while True:
    print(gnss.get_raw_data(ser))
    #lat, lon = gnss.get_lat_lon(ser)
    #print("lat:", lat, "lon:", lon)
    #num_sv, hdop = gnss.get_satellite_info(ser)
    #print("sat:", num_sv, "hdop:", hdop)
    time.sleep(0.1)