# https://stackoverflow.com/questions/7023052/configure-flask-dev-server-to-be-visible-across-the-network
# env FLASK_APP=flaskApp.py flask run --host=0.0.0.0

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

app.run(host='0.0.0.0')`



