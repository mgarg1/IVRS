# https://www.electronicwings.com/sensors-modules/mt8870-dtmf-decoder
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
import RPi.GPIO as GPIO

Q1,Q2,Q3,Q4,SDT = 29,31,33,35,37
INBITS = [Q1,Q2,Q3,Q4,SDT]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(INBITS, GPIO.IN)

def my_callback(unused_channel,testStr):
    print('rcvd callback')
    binStr = str(GPIO.input(Q4))+str(GPIO.input(Q3))+str(GPIO.input(Q2))+str(GPIO.input(Q1))
    decNum = int(binStr,2)
    print(decNum)

callback_rt = lambda x:my_callback(x,'HELLO')

GPIO.add_event_detect(SDT, GPIO.RISING, callback=callback_rt, bouncetime=200)

while True:
	pass
