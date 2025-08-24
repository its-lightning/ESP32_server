# main.py
import network
import machine
import time

# Set up ESP32 as an Access Point
ap = network.WLAN(network.AP_IF)   # Access Point mode
ap.active(True)
ap.config(essid='lights domain', password='bloodforthebloodgod')

print("Access Point configured!")
print("SSID:", ap.config('essid'))
print("IP address:", ap.ifconfig()[0])

# Blink onboard LED to show AP is active
led = machine.Pin(2, machine.Pin.OUT)

while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
