import json
from flask import Flask, Response
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
    motor.gogo()
    # story.main()
    return Response(json.dumps(result), mimetype='application/json')


# 讲故事
@app.route("/go")
def gogo():
    motor.gogo() 
    result = {'status': 'go'}
    return Response(json.dumps(result), mimetype='application/json')


@app.route("/stop")
def stop():
    motor.stop()
    result = {'status': 'stop'}
    return Response(json.dumps(result), mimetype='application/json')

@app.route("/back")
def back():
    motor.back()
    result = {'status': 'back'}
    return Response(json.dumps(result), mimetype='application/json')



# 启动app
app.run(port=8081, host='0.0.0.0')
