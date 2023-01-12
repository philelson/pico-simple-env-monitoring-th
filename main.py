import secrets
import config
import network
import time
import machine
from time import sleep
from environment_AHT20 import EnvironmentAHT20 as Environment
from picozero import pico_led
from umqttsimple import MQTTClient
from machine import Pin


# 
# Functions
#
def connect(ssid, password):
    pico_led.on()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    connectionAttemptLimit = 10
    connectionAttempts = 0
    while wlan.isconnected() == False:
        pico_led.off()
        print(f'Waiting for connection on {ssid}...')
        sleep(0.5)
        pico_led.on()
        sleep(0.5)
        connectionAttempts += 1
        if connectionAttempts >= connectionAttemptLimit: return False
    ip = wlan.ifconfig()[0]
    print(f'Connected to {ssid} on {ip}')
    return ip

def mqttConnect(mqtt_client_id, mqtt_server, mqtt_port, mqtt_username, mqtt_password):
    client = MQTTClient(mqtt_client_id, mqtt_server, mqtt_port, mqtt_username, mqtt_password)
    client.connect()
    print('Connected to %s MQTT Broker'%(config.mqtt_server))
    return client

def restartMachine():
    print('Failed to connected to services. Restarting...')
    time.sleep(5)
    machine.reset()

def tempHasChanged():
    currentTemp = Environment.getTemp()
    previousTemp = Environment.previousTemperature
    delta = (currentTemp - previousTemp)
    if delta < 0: delta = delta * -1
    hasChanged = delta >= config.temp_delta_threshold
    if hasChanged: 
        Environment.previousTemperature = currentTemp
        print(f'currentTemp {currentTemp}, previousTemp {previousTemp}, delta {delta}, threshold {config.temp_delta_threshold} hasChanged {hasChanged}')
    return hasChanged, currentTemp

def humidityHasChanged():
    currentHumidity = Environment.getRelativeHumidity()
    previousHumidity = Environment.previousHumidity
    delta = (currentHumidity - previousHumidity)
    if delta < 0: delta = delta * -1
    hasChanged = delta >= config.humidity_delta_threshold
    if hasChanged: 
        Environment.previousHumidity = currentHumidity
        print(f'currentHumidity {currentHumidity}, previousHumidity {previousHumidity}, delta {delta}, threshold {config.humidity_delta_threshold}, hasChanged {hasChanged}')
    return hasChanged, currentHumidity

def ledFlash():
    pico_led.on()
    sleep(0.1)
    pico_led.off()
    sleep(0.1)
    
#
# Main Program
# 
try:
    print('pico-simple-env-monitoring-th v0.0.1')
    ip = connect(secrets.ssid, secrets.password)
    if False == ip:
        ip = connect(secrets.ssid2, secrets.password2)
    elif False == ip:
        print(f'Unable to connect to {secrets.ssid} or {secrets.ssid2}')
    
    client = mqttConnect(config.mqtt_client_id, config.mqtt_server, config.mqtt_port, config.mqtt_username, config.mqtt_password)

    while True:
        tempData = tempHasChanged();
        humidityData = humidityHasChanged();

        if True == tempData[0]:
            client.publish(config.topic_temp_change, str(tempData[1]))
            ledFlash()
        if True == humidityData[0]:
            client.publish(config.topic_humidity_change, str(humidityData[1]))       
            ledFlash()
except KeyboardInterrupt:
    print('KeyboardInterrupt Error')
    restartMachine()
except OSError as e:
    print('OSError Error')
    restartMachine()
