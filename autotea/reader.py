from decimal import Decimal
import glob
import os


class TemperatureReader:
    def __init__(self, fail_loud=True):
        self.base_dir = "/sys/bus/w1/devices"
        self.fail_loud = fail_loud

        if not os.path.isdir(self.base_dir):
            self.__start_modprobe()

        try:
            device_folder = glob.glob(f"{self.base_dir}/28*")[0]
        except IndexError as e:
            raise IOError(
                "Could not locate device interface.  Please see the following link to make sure you've enbaled 1-wire interfaces: https://www.raspberrypi-spy.co.uk/2013/03/raspberry-pi-1-wire-digital-thermometer-sensor/."
            ) from e

        self.file_path = f"{device_folder}/w1_slave"

    def __start_modprobe(self):
        os.system("modprobe w1-gpio")
        os.system("modprobe w1-therm")

    def __read_raw(self):
        with open(self.file_path) as fo:
            return fo.readlines()

    def __format(self, raw_line):
        raw_temp = raw_line.strip()[raw_line.index("=") + 1 :]

        return Decimal(raw_temp) / Decimal(1000)

    def __crc_valid(self, crc_line):
        return crc_line.strip()[-3:] == "YES"

    def read(self):
        raw_data = self.__read_raw()

        if not self.__crc_valid(raw_data[0]):
            if self.fail_loud:
                raise ValueError(f"CRC Check failed. Raw data below:\n\n{raw_data}")
            else:
                return None

        return self.__format(raw_data[1])
