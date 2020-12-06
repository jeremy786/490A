import flask
import sys
from flask import request, jsonify,send_from_directory, redirect, url_for

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
        data= request.form["test"]
        print(data, flush=True)
    return jsonify(success=True)

@app.route("/kinect",methods=["POST"])
def kinect():
    result = request.get_json()
    print(result, flush=True)
    return jsonify(success=True)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
app.run()