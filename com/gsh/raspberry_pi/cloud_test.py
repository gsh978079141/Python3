import json
from flask import Flask, Response,request
# import story
import motor
app = Flask(__name__)


@app.route("/health")
def health():
    result = {'status': 'UP'}
    return Response(json.dumps(result), mimetype='application/json')


# 讲故事
@app.route("/tellStory")
def tellStory():
    result = {'username': 'gsh', 'password': 'gsh'}
    # story.main()
    return Response(json.dumps(result), mimetype='application/json')


# 讲故事
@app.route("/go",methods=["GET", "POST"])
def gogo():
    data = json.loads(request.data)
    sleepTime = data['time']
    motor.gogo(sleepTime)
    result = {'status': 'go'}
    return Response(json.dumps(result), mimetype='application/json')


@app.route("/stop",methods=["GET", "POST"])
def stop():
    motor.stop()
    result = {'status': 'stop'}
    return Response(json.dumps(result), mimetype='application/json')

@app.route("/back",methods=["GET", "POST"])
def back():
    data = json.loads(request.data)
    sleepTime = data['time']
    motor.back(sleepTime)
    result = {'status': 'back'}
    return Response(json.dumps(result), mimetype='application/json')


# 启动app
app.run(port=8081, host='0.0.0.0')
