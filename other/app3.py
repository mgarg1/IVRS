#!flask/bin/python
from flask import Flask
import sys
import datetime
import logging
import logging.handlers
import time
from multiprocessing import shared_memory

SHM_NAME='my_shm64'
shm_a = None
try:
    shm_a = shared_memory.SharedMemory(name=SHM_NAME,create=True, size=1)
    # type(shm_a.buf)
    buffer = shm_a.buf
    # len(buffer)
    buffer[0] = 255                           # Modify single byte at a time
except Exception as e:
    print(e)


logger = logging.getLogger('rootLogger')

sys.tracebacklimit = 0
# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
VENV_PYTHON = "../venv/bin/python"
# Path to the script that must run under the virtualenv
MAIN_SCRIPT = "state_pattern.py"

app = Flask(__name__)
myAppCtx = {'keepAlive': True}

def prepareMsg(msg):
    if not isinstance(msg, str):
        logger.critical('WRONG MESSAGE TYPE')
        return 'INVALID MESSAGE'

    return msg.replace('exitState:', '')

@app.route('/check_server', methods=['GET', 'POST'])
def check_server():
    return 'server is up',200

@app.route('/phoneNum/<string:phoneNum>', methods=['GET', 'POST'])
def show_post(phoneNum):
    # show the post with the given id, the id is an integer
    global myAppCtx

    myAppCtx['keepAlive'] = True
    phoneNum = str(phoneNum)
    phoneNum2 = phoneNum[-10:]  #last 10 digits
    # allMatch  = re.findall(r"\d{10}", phoneNum2)


    logger.info('PhoneNum - %s & PhoneNum2 - %s', phoneNum, phoneNum2)
    retVal='Nothing returned from main'
    retVal='exitState:Apt Cancelled'
    retVal='no response exit'
    retVal='exitState:Apt Confirmed'

    # Attach to an existing shared memory block
    shm_b = shared_memory.SharedMemory(SHM_NAME)
    buf1 = shm_b.buf
    print('bufer value---->  ' + str(int(buf1[0])))

    while int(buf1[0])==255:
        pass

    buf1[0] = 255
    shm_b.close()
    # time.sleep(30)shm_b.buf[0]

    #The try block does not raise any errors, so the else block is executed:
    #try:
    #   retVal = main4(phoneNum2, myAppCtx)
    #except NameError as nm:
    #    logger.error('Exception in main4: %s', nm)
    #except Exception as ExceptionStr:
    #    logger.error('Exception in main4:  %s',ExceptionStr)
    #else:
    #    logger.debug('no Exception Raised in main4')
    
    logger.critical('TIME OVER')
    return prepareMsg(retVal), 200

@app.route('/kilall', methods=['GET', 'POST'])
def kill_all_process():
    global myAppCtx
    logger.critical('----- Killing All processes ----')
    
    # Attach to an existing shared memory block
    shm_c = shared_memory.SharedMemory(SHM_NAME)
    buf1 = shm_c.buf
    buf1[0] = 0
    # print(int(shm_b.buf[0])==0)
    shm_c.close()

    myAppCtx['keepAlive'] = False
    return 'Success', 400

@app.route('/', methods=['GET'])
def default_route():
    # show the post with the given id, the id is an integer
    logger.critical('invalid url')
    return 'hello'


if __name__ == '__main__':
    LOG_FILENAME='logging.conf'
    # https://docs.python.org/3/library/logger.html#logrecord-attributes
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d >>> %(message)s', level=logging.DEBUG)
    # Add the log message handler to the logger
    
    # handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*50, backupCount=2) #50MB
    # logger.addHandler(handler)
    # logger.setLevel(logging.DEBUG)

    # logger.fileConfig('./logging.conf')
    # gpio_initialize()
    try:
        app.run(debug=True, host='0.0.0.0', port=10100, threaded=False, processes=5)
    except Exception as e:
        print(e)
    finally:
        shm_a.close()
        shm_a.unlink()
