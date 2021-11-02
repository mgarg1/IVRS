import RPi.GPIO as GPIO
import logging
import time

logger = logging.getLogger('rootLogger')

# Q1,Q2,Q3,Q4,SDT = 8,10,12,16,18
Q1, Q2, Q3, Q4, SDT = 29, 31, 33, 35, 37
INBITS = [Q1, Q2, Q3, Q4, SDT]
GSM_RST = 12
GSM_PWR = 11
OUTBITS = [GSM_RST, GSM_PWR]

def gsm_rst():
    GPIO.output(GSM_RST, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GSM_RST, GPIO.LOW)
    # time.sleep(10)
    print('gsm reset done')


def gsm_power_on():
    GPIO.output(GSM_PWR, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GSM_PWR, GPIO.LOW)
    print('gsm power on')
    

def gpio_initialize():
    logger.debug(' gpio_init called-*')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INBITS, GPIO.IN)
    GPIO.setup(OUTBITS, GPIO.OUT)

def read_dtmf():
    in3, in2, in1, in0 = GPIO.input(Q4), GPIO.input(Q3), GPIO.input(Q2), GPIO.input(Q1)
    decNum = 0
    decNum = decNum | ( in3 << 3) | ( in2 << 2) | ( in1 << 1) | ( in0 << 0)
    strList = '01234567890*#'
    # print('int key pressed - ' + str(decNum))
    # if decNum >= 0 and decNum < len(strList):
    
    if 0 <= decNum < len(strList):
        return strList[decNum]

    logger.critical('invalid key pressed - %d',decNum)
    return None


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
