from picozero import pico_temp_sensor

class EnvironmentInterface:
    previousTemperature = 0;
    previousHumidity = 0;

    def getTemp():
        return pico_temp_sensor.temp

    def getRelativeHumidity():
        return -1





