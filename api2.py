from asyncio.tasks import sleep
import flask
import sys
import time
import datetime
import asyncio
import serial
import io
from datetime import date, datetime
# import RPi.GPIO as GPIO
from flask import request, jsonify,send_from_directory, redirect, url_for
from flask import make_response

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(24, GPIO.OUT)
# GPIO.output(24, 1)

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

imuData = []
scaleData = []
watchData = []
kinectData = []
global watchSerial,scaleSerial,IMUSerial

def watchTestRead():
    while True:
        watchData = []
        print("Polling watch starting",flush=True)
        for x in range(10):
            if(len(watchData) > 10):
                watchData.pop()
            watchData.append(watchSerial.readline())
        print("polling finished\nData:",flush=True)
        for x in range(10):
            print(watchData[x],flush=True)

def IMU_READ():
    bluetoothSerial = serial.Serial("/dev/rfcomm0",baudrate=9600)
    #sio = io.TextIOWrapper(io.BufferedRWPair(bluetoothSerial,bluetoothSerial))
    print("Bluetooth IMU connected",flush=True)
    global imuData
    imuData = []
    try:
        while len(imuData) < 5:
            #sio.flush()
            #data = sio.readline()
            data = bluetoothSerial.readline()
            print(data,flush=True)
            now = datetime.now()
            imuData.append({now.strftime("%H:%M:%S"):"Time"})
    except:
        print("did not connect",flush=True)
    # await asyncio.sleep(10)
    # for x in range(5):
    #     now = datetime.now()
    #     print({now.strftime("%H:%M:%S"):x})
    #     imuData.append({now.strftime("%H:%M:%S"):x})

def SCALE_READ():
    bluetoothSerial = serial.Serial("/dev/rfcomm2",baudrate=9600)
    print("Bluetooth SCALE connected",flush=True)
    global scaleData
    scaleData = []
    try:
        while len(scaleData) < 5:
            data = bluetoothSerial.readline()
            print(data,flush=True)
            now = datetime.now()
            scaleData.append({now.strftime("%H:%M:%S"):"Time"})
    except:
        print("did not connect",flush=True)
    # await asyncio.sleep(10)
    # for x in range(5):
    #     now = datetime.now()
    #     print({now.strftime("%H:%M:%S"):x})
    #     scaleData.append({now.strftime("%H:%M:%S"):x})


def WATCH_READ():
    bluetoothSerial = serial.Serial("/dev/rfcomm3",baudrate=9600)
    print("Watch connected",flush=True)
    global scaleData
    scaleData = []
    try:
        while len(scaleData) < 5:
            data = bluetoothSerial.readline()
            print(data,flush=True)
            now = datetime.now()
            scaleData.append({now.strftime("%H:%M:%S"):"Time"})
    except:
        print("did not connect",flush=True)

#BLUETOOTH SETUP START
############
##########
def bluetoothSetup():
    global watchSerial,scaleSerial,IMUSerial
    watchSerial = serial.Serial("/dev/rfcomm3",baudrate=9600)
    print("Watch connected",flush=True)
    scaleSerial = serial.Serial("/dev/rfcomm2",baudrate=9600)
    print("Bluetooth SCALE connected",flush=True)
    #IMUSerial = serial.Serial("/dev/rfcomm0",baudrate=9600)
    print("Bluetooth IMU connected",flush=True)


#SERVER SETUP
#########
#########
app = flask.Flask(__name__)
app.config["DEBUG"] =  True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
@app.route("/",methods=["GET"])
def home():
    return "<h1>Welcome</h1>"


@app.route("/api/v1/imu",methods=["GET"])
def imu():
        IMU_READ()
        return jsonify(imuData)

@app.route("/api/v1/scale",methods=["GET"])
def scale():
        SCALE_READ()
        return jsonify(scaleData)

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
        # GPIO.output(24,0)
        time.sleep(float(request.form["time"]))
        # GPIO.output(24,1)
    return make_response(jsonify(data),200)

@app.route('/app/v1/trackingData', methods=["GET"])
def tracking_data():
    return make_response(jsonify(kinectData.pop(-1),200)

@app.route("/kinect",methods=["POST"])
def kinect():
    result = request.get_json()
    print(result, flush=True)
    #if(len(kinectData > 5)
    #    kinectData.pop(0)
    kinectData.append(result)
    return make_response(jsonify(result),200)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
app.run(host="0.0.0.0",port=8080)
#bluetoothSetup()
#watchTestRead()
