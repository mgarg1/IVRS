import RPi.GPIO as GPIO
import logging

logger = logging.getLogger('rootLogger')

# Q1,Q2,Q3,Q4,SDT = 8,10,12,16,18
Q1, Q2, Q3, Q4, SDT = 29, 31, 33, 35, 37
INBITS = [Q1, Q2, Q3, Q4, SDT]


def gpio_initialize():
    logger.debug(' gpio_init called-*')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INBITS, GPIO.IN)


def read_dtmf():
    logger.debug('key pressed')
    binStr = str(GPIO.input(Q4))+str(GPIO.input(Q3))+str(GPIO.input(Q2))+str(GPIO.input(Q1))
    decNum = int(binStr, 2)
    if decNum == 10:
        decNum = 0
    return str(decNum)


def register_callback(callback_rt):
    GPIO.add_event_detect(SDT, GPIO.RISING, callback=callback_rt, bouncetime=200)

def remove_callback():
    GPIO.remove_event_detect(SDT)

def gpio_clean():
    # GPIO.remove_event_detect(SDT)
    logger.debug(' gpio_clean called-*')
    try:
        GPIO.cleanup()
    except Exception as e:
        logger.debug('caught exception in gpio_clean - %s',str(e))
    else:
        logger.debug('gpio_clean doesnt raise exception')
