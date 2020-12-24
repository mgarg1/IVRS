import os

FIFO='myfifo1'

def fun1():
    while True:
        with open(FIFO, 'rt') as fifo:
            inRes = fifo.readline()
            if len(inRes) == 0:
                print('invalid data;')
                continue
            print(inRes)

fun1()

