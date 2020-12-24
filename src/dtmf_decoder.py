# https://www.electronicwings.com/sensors-modules/mt8870-dtmf-decoder
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
import RPi.GPIO as GPIO

Q1,Q2,Q3,Q4,SDT = 8,10,12,16,18
INBITS = [Q1,Q2,Q3,Q4,SDT]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(INBITS, GPIO.IN)

FIFO = 'myfifo1'

def my_callback(*unused_channel):
    binStr = str(GPIO.input(Q4))+str(GPIO.input(Q3))+str(GPIO.input(Q2))+str(GPIO.input(Q1))
    decNum = int(binStr,2)
    print(decNum)
    with open('myfifo1','wt') as fifo:
        fifo.write(str(decNum))

GPIO.add_event_detect(SDT, GPIO.RISING, callback=my_callback, bouncetime=200)
#GPIO.remove_event_detect(SDT)

#def f(q):
#    q.put([42, None, 'hello'])
#
#if __name__ == '__main__':
#    q = Queue()
#    p = Process(target=f, args=(q,))
#    p.start()
#    print(q.get())    # prints "[42, None, 'hello']"
#    p.join()


# GPIO.setup(OUTBITS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.output(25, GPIO.input(4))
# int('11111111', 2)
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
