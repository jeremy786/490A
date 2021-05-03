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
    #bluetoothSerial = serial.Serial("/dev/rfcomm3",baudrate=9600)
    global watchData
    watchData = []
    print("Polling watch starting",flush=True)
    try:
        print("test1")
        while len(watchData) < 5:
            print("test2")
            data = watchSerial.readline()
            print(data,flush=True)
    except:
        print("did not work")

def IMU_READ():
    #bluetoothSerial = serial.Serial("/dev/rfcomm0",baudrate=9600)
    #print("Bluetooth IMU connected",flush=True)
    global imuData
    imuData = []
    try:
        while len(imuData) < 5:
            data = imuSerial.readline()
            print(data,flush=True)
            imuData.append({"line":data.decode("utf-8")})
            if len(imuData) > 5:
               imuData.pop()
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
            print("test")
            data = blueToothSerial.readline()
            print(data,flush=True)
            #scaleData.append({"line":data.decode("utf-8")})
            if len(scaleData) > 5:
                scaleData.pop()
            #scaleData.append({"Time":now.strftime("%H:%M:%S"),"weight":data})
    except:
        print("did not connect",flush=True)
    # await asyncio.sleep(10)
    # for x in range(5):
    #     now = datetime.now()
    #     print({now.strftime("%H:%M:%S"):x})
    #     scaleData.append({now.strftime("%H:%M:%S"):x})
def WATCH_READ():
    #bluetoothSerial = serial.Serial("/dev/rfcomm3",baudrate=9600)
    print("Watch connected",flush=True)
    global watchData
    watchData = []
    try:
        while len(watchData) < 5:
            data = watchSerial.readline()
            print(data,flush=True)
            watchData.append({"line":data.encode("utf-8")})
            if len(watchData) > 5:
               watchData.pop()
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
    IMUSerial = serial.Serial("/dev/rfcomm0",baudrate=9600)
    print("Bluetooth IMU connected",flush=True)


#SERVER SETUP
#########
#########
app = flask.Flask(__name__)
app.config["DEBUG"] =  False
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

@app.route("/api/v1/watch",methods=["GET"])
def watch():
        WATCH_READ()
        return jsonify(watchData)

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
    return make_response(kinectData[-1],200)

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

#bluetoothSetup()
#app.run(host="0.0.0.0",port=8080)
#watchTestRead()
SCALE_READ()
