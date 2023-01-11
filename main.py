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

def mqttReconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

def tempHasChanged():
    currentTemp = Environment.getTemp()
    previousTemp = Environment.previousTemperature
    delta = (currentTemp - previousTemp)
    if delta < 0: delta = delta * -1
    hasChanged = delta >= config.temp_delta_threshold
    if hasChanged: print(f'currentTemp {currentTemp}, previousTemp {previousTemp}, delta {delta}, threshold {config.temp_delta_threshold} hasChanged {hasChanged}')
    return hasChanged

def humidityHasChanged():
    currentHumidity= Environment.getRelativeHumidity()
    previousHumidity = Environment.previousHumidity
    delta = (currentHumidity - previousHumidity)
    if delta < 0: delta = delta * -1
    hasChanged = delta >= config.humidity_delta_threshold
    if hasChanged: print(f'currentHumidity {currentHumidity}, previousHumidity {previousHumidity}, delta {delta}, threshold {config.humidity_delta_threshold}, hasChanged {hasChanged}')
    return hasChanged

def ledFlash():
    pico_led.on()
    sleep(0.1)
    pico_led.off()
    sleep(0.1)
#
# Main Program
# 
try:
    ip = connect(secrets.ssid, secrets.password)
    if False == ip:
        ip = connect(secrets.ssid2, secrets.password2)
    elif False == ip:
        print(f'Unable to connect to {secrets.ssid} or {secrets.ssid2}')
    
    client = mqttConnect(config.mqtt_client_id, config.mqtt_server, config.mqtt_port, config.mqtt_username, config.mqtt_password)

    while True:
        if True == tempHasChanged():
            currentTemp = Environment.getTemp();
            Environment.previousTemperature = currentTemp
            client.publish(config.topic_temp_change, str(Environment.getTemp()))
            ledFlash()
        if True == humidityHasChanged():
            currentHumidity = Environment.getRelativeHumidity()
            Environment.previousHumidity = currentHumidity
            client.publish(config.topic_humidity_change, str(currentHumidity))       
            ledFlash()
except KeyboardInterrupt:
    print('Error')
    machine.reset()
