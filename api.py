import flask
import sys
import time
import RPi.GPIO as GPIO
from flask import request, jsonify,send_from_directory, redirect, url_for
from flask import make_response

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, 1)

test = [{
    "key":"val",
    "key2":"val2"
},
{
    "key3":"val3",
    "key4":"val4"
},{
    "ke5":"val5",
    "key6":"val6"
},
]

app = flask.Flask(__name__)
app.config["DEBUG"] =  True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
@app.route("/",methods=["GET"])
def home():
    return "<h1>Welcome</h1>"



@app.route("/api/v1/test",methods=["GET"])
def api_test():
        return jsonify(test)

@app.route('/form', methods=['GET', 'POST'])
def form_test():
    if request.method == "GET":
        return app.send_static_file('form.html')
    else:
        data= request.form
        print(data["text"], flush=True)
        GPIO.output(24,0)
        time.sleep(float(request.form["time"]))
        GPIO.output(24,1)
    return make_response(jsonify(data),200)

@app.route("/kinect",methods=["POST"])
def kinect():
    result = request.get_json()
    print(result, flush=True)
    GPIO.output(24,0)
    time.sleep(0.5)
    GPIO.output(24,1)
    return make_response(jsonify(result),200)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
app.run(host="0.0.0.0",port=8080)
