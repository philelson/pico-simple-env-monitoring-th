from environment__ import EnvironmentInterface
import utime
from machine import Pin, I2C
import ahtx0

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
        return EnvironmentAHT20.sensor.temperature;

    def getRelativeHumidity():
        EnvironmentAHT20.initI2C()
        return EnvironmentAHT20.sensor.relative_humidity


