#!flask/bin/python
from flask import Flask, jsonify
import subprocess
# from subprocess import Popen,PIPE
import re
from ivrs_utils import killtree
from state_pattern import main4
import sys
from dtmf_decoder3 import gpio_initialize
sys.tracebacklimit = 0
# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
VENV_PYTHON = "../venv/bin/python"
# Path to the script that must run under the virtualenv
MAIN_SCRIPT = "state_pattern.py"


app = Flask(__name__)
gpio_initialize()
oldProcessId=None

@app.route('/phoneNum/<string:phoneNum>', methods=['GET','POST'])
def show_post(phoneNum):
    # show the post with the given id, the id is an integer
    global oldProcessId

    if oldProcessId:
        killtree(oldProcessId)
        oldProcessId = None

    phoneNum  = str(phoneNum)
    phoneNum2  = phoneNum[-10:] #last 10 digits
    allMatch  = re.findall("\d{10}", phoneNum2)

    print('PhoneNum - ' + phoneNum + ' & PhoneNum2 - ' + phoneNum2)

    #The try block does not raise any errors, so the else block is executed:
    try:
        retVal = main4(phoneNum2)
    except Exception as ExceptionStr:
        print(ExceptionStr)
        # if ExceptionStr.find('exitState'):
        #     print('exitState found\n')
        #     return ExceptionStr.replace('exitState:',''),200
        # elif ExceptionStr.find('no response exit'):
        #     print('found no response\n')
    else:
        print('no Exception Raised\n')
        print(retVal)
        return 'Sucess',200

    return 'Command Not known',501


@app.route('/kilall', methods=['GET','POST'])
def kill_all_process():
    #kill all the running process
    global oldProcessId
    if oldProcessId:
        killtree(oldProcessId)
        oldProcessId = None
    return 'Success',400


@app.route('/', methods=['GET'])
def default_route():
    # show the post with the given id, the id is an integer
    print('invalid url')
    return 'hello'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=10100)


