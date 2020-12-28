#!flask/bin/python
from flask import Flask, jsonify
import subprocess
# from subprocess import Popen,PIPE
import re
from ivrs_utils import killtree
from state_pattern import main3

# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
VENV_PYTHON = "../venv/bin/python"
# Path to the script that must run under the virtualenv
MAIN_SCRIPT = "state_pattern.py"


app = Flask(__name__)

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

    try:
        main3()
    except Exception as ExceptionStr:
        if ExceptionStr.find('exitState'):
            print('found')
            return ExceptionStr.replace('exitState:',''),200
    
    # print('123' + ToDoc)

    # p1 = subprocess.Popen([VENV_PYTHON,MAIN_SCRIPT,phoneNum2], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
    # oldProcessId=p1.pid
    # #stdout1, stderr1 = p1.communicate()
    # #print(str(stdout1.decode()))
    # p1.stdout.flush()
    
    # while p1.poll() == None:
    #     line = p1.stdout.readline()
    #     #line = line.decode(encoding='utf-8')
    #     if not line:
    #         print('invalid/blank line')
    #         continue
    #     elif line.find('exitState') != -1: 
    #         print('pinned line - ' + line)
    #         return line.replace('exitState:',''),200

    # print("test:", line.rstrip())

    return 'Command Not known',501


@app.route('/kilall', methods=['GET','POST'])
def kill_all_process():
    #kill all the running process
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


