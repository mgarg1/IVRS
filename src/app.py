#!flask/bin/python
from flask import Flask, jsonify
from subprocess import Popen,PIPE
import re

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


@app.route('/phoneNum/<string:phoneNum>', methods=['GET','POST'])
def show_post(phoneNum):
    # show the post with the given id, the id is an integer

    phoneNum  = str(phoneNum)
    phoneNum2  = phoneNum[-10:] #last 10 digits
    allMatch  = re.findall("\d{10}", phoneNum2)

    if allMatch:
        print('recvd PhoneNum' + phoneNum)
    else:
        #print('phone Num correct1' + phoneNum)
        print('phone Num correct2' + phoneNum2)
   
    # Path to a Python interpreter that runs any Python script
    # under the virtualenv /path/to/virtualenv/
    python_bin = "../venv/bin/python"
    
    # Path to the script that must run under the virtualenv
    script_file = "state_pattern.py"

    session = Popen([python_bin,script_file,phoneNum2], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()

    # get output from process "Something to print"
    one_line_output = p.stdout.readline()
    while one_line_output:
        print(one_line_output)
        one_line_output = p.stdout.readline()


    if stderr:
        raise Exception("Error "+str(stderr))
    #return stdout.decode('utf-8')
    
    
    return 'hello'


@app.route('/', methods=['GET'])
def default_route():
    # show the post with the given id, the id is an integer
    print('invalid url')
    return 'hello'



@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=10100)
