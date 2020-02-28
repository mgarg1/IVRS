# https://www.electronicwings.com/sensors-modules/mt8870-dtmf-decoder
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# python -m virualenv proj/ --no-download -p python3
# sudo apt-get install libjpeg-dev zlib1g-dev
# pip install python-escpos --no-cache-dir
# sudo apt-get install python3-rpi.gpio
# https://python-escpos.readthedocs.io/en/latest/user/raspi.html

import RPi.GPIO as GPIO
import time
from escpos.printer import Usb
from datetime import datetime

SW1 = 8
LED1 = 10
LED2 = 12

TOKEN_START = 12
TOKEN_DELTA = 2
LAST_TOKEN_FILENAME = "lastToken.txt"
LAST_DATE_FILENAME = "lastDate.txt"

def setupFiles(filename):
    with open(filename,'a',encoding = 'utf-8') as f:
        pass

def getNextTokenNumber():
    with open(LAST_DATE_FILENAME,'r+',encoding = 'utf-8') as dateFile:
        lastDay = dateFile.read().strip()
        now = datetime.now() # current date and time
        now_day = now.strftime("%d-%b-%Y").strip()

        lastToken = TOKEN_START    
        with open(LAST_TOKEN_FILENAME,'r+',encoding = 'utf-8') as tokenFile:
            # print(now_day)
            # print(lastDay)
            if lastDay == now_day:
                # print("day hasn't changed")
                lastToken = tokenFile.read()
                lastToken = int(lastToken) + TOKEN_DELTA
            
            tokenFile.truncate(0)
            tokenFile.seek(0)
            tokenFile.write(str(lastToken))
        dateFile.truncate(0)
        dateFile.seek(0)
        dateFile.write(now_day)
        return lastToken

def setupPrinter():
    # try:
        printerObj = Usb(0x0456, 0x0808, 0, 0x81, 0x03)
        # printerObj.panel_buttons(enable=False)
        return printerObj
    # except USBNotFoundError as errorMsg:
    #     print(errorMsg)

def printDate(printerObj):
    now = datetime.now() # current date and time
    now_time = now.strftime("%d-%b-%Y         %H:%M:%S")
    printerObj.set(height=1, width=1)
    printerObj.text(now_time)
    printerObj.control("CR")

def printToken(printerObj,tokenCount):
    printerObj.hw("INIT")
    printerObj.control("LF")
    printDate(printerObj)    
    
    printerObj.image("sleet3.png",impl="bitImageColumn")
    printerObj.set(width=3,align='center')
    printerObj.text(tokenCount)
    printerObj.text("\n\n")
    printerObj.image("footer.png",impl="bitImageColumn")
    # TODO : not sure if it needs to be here
    # printerObj.set(font='a', height=1, width=1, align='center')
    printerObj.text("\n\n\n\n")
    # printerObj.print_and_feed(n=1)
    printerObj.hw("INIT")
    # printerObj.cut()

def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # GPIO.setup(OUTBITS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    # GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(LED1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW)


def mainLoop():
    setupGPIO()
    printerObj = setupPrinter()
    setupFiles(LAST_DATE_FILENAME)
    setupFiles(LAST_TOKEN_FILENAME)

    try:
        while True: # Run forever
            GPIO.output(LED1, GPIO.HIGH)
            GPIO.output(LED2, GPIO.LOW)
            # time.sleep(5)
            if GPIO.input(SW1) == GPIO.HIGH:
                GPIO.output(LED2, GPIO.HIGH)
                GPIO.output(LED1, GPIO.LOW)
                printToken(printerObj,str(getNextTokenNumber()))
                print("Button was pushed!")
                time.sleep(5)

    except KeyboardInterrupt:
        GPIO.cleanup()

mainLoop()
# def my_callback(arg1):
#   print int(str(GPIO.input(Q4))+str(GPIO.input(Q3))+str(GPIO.input(Q2))+str(GPIO.input(Q1)),2)

# GPIO.output(25, GPIO.input(4))
# int('11111111', 2)
# GPIO.add_event_detect(SDT, GPIO.RISING)
# GPIO.add_event_callback(SDT, my_callback)
# GPIO.add_event_detect(22, GPIO.RISING, callback=my_call)
# GPIO.add_event_detect(SDT, GPIO.RISING)
# GPIO.wait_for_edge(SDT, GPIO.RISING)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
# GPIO.add_event_detect(SDT, GPIO.FALLING)
# GPIO.add_event_detect(4, GPIO.BOTH)
# GPIO.add_event_callback(4, my_callback)
# GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback) 

# while True:
    # pass