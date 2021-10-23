#!flask/bin/python
from flask import Flask
from ivrs_utils import sendMessageToTelegram, postMessageToPasteBin
from state_pattern import main4, SHM_NAME
from multiprocessing import shared_memory

# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
VENV_PYTHON = "../venv/bin/python"
# Path to the script that must run under the virtualenv
MAIN_SCRIPT = "state_pattern.py"

app = Flask(__name__)
myAppCtx = {'keepAlive': True}

@app.route('/killall', methods=['GET', 'POST'])
def kill_all_process():
    global myAppCtx
    # logger.critical('----- Killing All processes ----')
    myAppCtx['keepAlive'] = False
     # Attach to an existing shared memory block
    shm_c = shared_memory.SharedMemory(SHM_NAME)
    buf1 = shm_c.buf
    buf1[0] = 0
    # print(int(shm_b.buf[0])==0)
    shm_c.close()
    return 'Success', 400

@app.route('/', methods=['GET'])
def default_route():
    # show the post with the given id, the id is an integer
    # logger.critical('invalid url')
    return 'hello'


if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=10101, threaded=False, processes=1)
    except Exception as e:
        print(e)