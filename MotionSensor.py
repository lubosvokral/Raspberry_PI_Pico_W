import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin
import machine
import time, utime
import urequests as requests

led = Pin("LED", Pin.OUT)

sensor_pir = Pin(28, Pin.IN, Pin.PULL_DOWN)
led_yellow = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.Pin(16, machine.Pin.OUT)

ssid = 'Lubik'
password = 'heslo1234'
ifttt_key = "Lvj4ud_ADTMv6Ddk9LINq"

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


def blick():
    for i in range(3):
        led.on()
        sleep(0.4)
        led.off()
        sleep(0.4)
    

def pir_handler():
    print("ALARM! Někdo prochází!")
    for i in range(30):
        led_yellow.toggle()
        buzzer.toggle()
        utime.sleep_ms(100)
        


ip = connect()
connection = open_socket(ip)
blick()

       
currentstate = 0
previousstate = 0

try:
    print("Čekám na aktivaci sensoru")
    while sensor_pir.value() == 1:
        currentstate = 0
    print("Sensor je připraven")
    
    while True:
        currentstate = sensor_pir.value()
        if currentstate == 1 and previousstate == 0:
            pir_handler()
            ifttt_url = "https://maker.ifttt.com/trigger/Pico_Motion_sensor/json/with/key/Lvj4ud_ADTMv6Ddk9LINq"
            request = requests.get(ifttt_url)
            print(request.content)
            request.close()
            previousstate = 1
            print("Počkám 10 vteřin na aktivaci sensoru")
            time.sleep(10)
        elif currentstate == 0 and previousstate == 1:
            print("Hotovo")
            previousstate = 0
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Quit")
