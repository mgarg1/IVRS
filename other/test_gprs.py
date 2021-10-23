import serial
import RPi.GPIO as GPIO
import os, time
GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
port.flush()
st1='AT\r\n'
st1='AT+COPS?\r\n' # get list of networks
port.write(st1.encode())
rcv = port.read(100)
print(rcv)
time.sleep(1)
