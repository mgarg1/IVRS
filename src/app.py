#!flask/bin/python
from flask import Flask
import sys,re,requests,subprocess,datetime
from ivrs_utils import killtree,sendMessageToTelegram,postMessageToPasteBin
from state_pattern import main4
from dtmf_decoder3 import gpio_initialize,gpio_clean
from dataAccess import allAptsOnDate,removeStaleBooking,addHoliday
import constants
from sensitive import PASTEBIN_API_KEY
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

sys.tracebacklimit = 0
# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
VENV_PYTHON = "../venv/bin/python"
# Path to the script that must run under the virtualenv
MAIN_SCRIPT = "state_pattern.py"

app = Flask(__name__)
gpio_initialize()

myAppCtx={'keepAlive':True}

def prepareMsg(msg):
    if type(msg) != str:
        logging.error('WRONG MESSAGE TYPE')
        return 'INVALID MESSAGE'

    return msg.replace('exitState:','')

@app.route('/check_server', methods=['GET','POST'])
def check_server():
    return 'server is up',200

@app.route('/phoneNum/<string:phoneNum>', methods=['GET','POST'])
def show_post(phoneNum):
    # show the post with the given id, the id is an integer
    global myAppCtx

    myAppCtx['keepAlive'] = True
    phoneNum  = str(phoneNum)
    phoneNum2  = phoneNum[-10:] #last 10 digits
    # allMatch  = re.findall(r"\d{10}", phoneNum2)

    logging.info('PhoneNum - %s & PhoneNum2 - %s' + phoneNum,phoneNum2)
    retVal='Nothing returned from main'
    #The try block does not raise any errors, so the else block is executed:
    try:
        retVal = main4(phoneNum2,myAppCtx)
    except Exception as ExceptionStr:
        logging.error(ExceptionStr)
    finally:
        gpio_clean()

    logging.info('no Exception Raised')
    return prepareMsg(retVal),200

@app.route('/cmd/PUB/', methods=['GET','POST'])
@app.route('/cmd/PUB/<string:dateOfApt>', methods=['GET','POST'])
def publish_list(dateOfApt=None):
    if dateOfApt == None:
        dateOfApt=datetime.datetime.now().strftime(constants.DATE_FORMAT)
    else:
        try:
            datetime.datetime.strptime(dateOfApt, constants.DATE_FORMAT)
        except ValueError:
            return "Error:Incorrect data format, should be DD-Month-YYYY",200
        
    apt_data_text = allAptsOnDate(dateOfApt)
    logging.info('appointment data -> %s', apt_data_text)
    if apt_data_text and apt_data_text != '':
        r = sendMessageToTelegram(apt_data_text)
        if r.status_code == 200:
            return 'pls visit ' + r.text,400
        
        logging.error('Error in posting to Telegram, trying SMS instead')
        
        r = postMessageToPasteBin(apt_data_text)
        
        if r.status_code == 200:
            return 'pls visit ' + r.text,200
        else:
            logging.error(r.text)
            return 'Error:error in posting to pastebin',200
    else:
        logging.info('No appointments for this date')
        return 'No appointments for this date',200

@app.route('/cmd/REM/', methods=['GET','POST'])
@app.route('/cmd/REM/<string:oldDate>', methods=['GET','POST'])
def remove_db_entries(oldDate=None):
    logging.info('----- removing entries from DB ----')
    if oldDate == None:
        oldDate=datetime.datetime.now().strftime(constants.DATE_FORMAT)
    else:
        try:
            datetime.datetime.strptime(oldDate, constants.DATE_FORMAT)
        except ValueError:
            return "Error:Incorrect data format, should be DD-Month-YYYY",200
    
    removeStaleBooking(oldDate)
    return 'Success',400

@app.route('/cmd/HOL/', methods=['GET','POST'])
@app.route('/cmd/HOL/<string:holDate>', methods=['GET','POST'])
def add_holiday(holDate=None):
    logging.info('----- adding holiday to DB ----')
    if holDate == None:
        holDate=datetime.datetime.now().strftime(constants.DATE_FORMAT)
    else:
        try:
            datetime.datetime.strptime(holDate, constants.DATE_FORMAT)
        except ValueError:
            return "Error:Incorrect data format, should be DD-Month-YYYY",200
    
    addHoliday(holDate)
    return 'Success',400

@app.route('/kilall', methods=['GET','POST'])
def kill_all_process():
    
    logging.info('----- Killing All processes ----')
    myAppCtx['keepAlive'] = False
    return 'Success',400

@app.route('/', methods=['GET'])
def default_route():
    # show the post with the given id, the id is an integer
    logging.warn('invalid url')
    return 'hello'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=10100)


