from sim800l import SIM800L
from dtmf_decoder3 import gpio_initialize, gsm_power_on
import time

# gpio_clean, gsm_rst,

sim800l=SIM800L('/dev/serial0',9600)
#sim800l=SIM800L('/dev/ttyAMA0')
sim800l.setup()

def answerCall(callerId):
    sim800l.answer_call()
    time.sleep(5)
    sim800l.send_sms('+919660813119','TEST MEssage')
    print('message sent')
    # time.sleep(5)
    sim800l.end_call()

def main4():
    gpio_initialize()
    gsm_power_on()
    sim800l.callback_incoming(answerCall)
    # sim800l.callback_no_carrier(checkEndCall)
    
    while True:
        sim800l.check_incoming()

main4()