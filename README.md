# Summary

PICO W code for reading humidity and temp data from a ATH20 sensor and sending data to MQTT when a change in either is detected. 

# Settings

Rename secrets.py.sample to secrets.py and enter wifi credentials
Rename config.py.sample to config.py and update MQTT settings

# Debugging

Data is logged to the terminal to provide debugging
Assuming mosquite MQTT the below will allow you to monitor incoming data changes (one for each temp and humidity topic)

```bash
mosquitto_sub -h {host} -t "{topic}" -u {username} -P {password}
```