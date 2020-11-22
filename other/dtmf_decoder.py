# https://www.electronicwings.com/sensors-modules/mt8870-dtmf-decoder
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
import RPi.GPIO as GPIO

Q1 = 32
Q2 = 36
Q3 = 38
Q4 = 40
SDT = 22
OUTBITS = [Q1,Q2,Q3,Q4,SDT]

GPIO.setmode(GPIO.BOARD)
# GPIO.setup(OUTBITS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OUTBITS, GPIO.IN)

def my_callback(arg1):
	print(int(str(GPIO.input(Q4))+str(GPIO.input(Q3))+str(GPIO.input(Q2))+str(GPIO.input(Q1)),2))

# GPIO.output(25, GPIO.input(4))
# int('11111111', 2)
GPIO.add_event_detect(SDT, GPIO.RISING)
GPIO.add_event_callback(SDT, my_callback)
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

while True:
	pass