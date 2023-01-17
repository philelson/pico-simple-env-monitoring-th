from environment__ import EnvironmentInterface
from machine import Pin, I2C
import utime
import ahtx0
import config

# https://github.com/targetblank/micropython_ahtx0
class EnvironmentAHT20(EnvironmentInterface):        
    sensor = None

    def initI2C():
        if EnvironmentAHT20.sensor is not None:
            return

        # I2C for the Wemos D1 Mini with ESP8266
        i2c = I2C(0, scl=Pin(1), sda=Pin(0))

        # Create the sensor object using I2C
        EnvironmentAHT20.sensor = ahtx0.AHT20(i2c)
    
    def getTemp():
        EnvironmentAHT20.initI2C()
        dataReading = EnvironmentAHT20.sensor.temperature
        return dataReading + config.temp_calibration_correction

    def getRelativeHumidity():
        EnvironmentAHT20.initI2C()
        dataReading = EnvironmentAHT20.sensor.relative_humidity
        return dataReading + config.humidity_calibration_correction



