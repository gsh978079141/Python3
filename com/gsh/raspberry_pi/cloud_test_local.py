import json
from flask import Flask, Response,request
import time
app = Flask(__name__)


@app.route("/health")
def health():
    result = {'status': 'UP'}
    return Response(json.dumps(result), mimetype='application/json')


# 讲故事
@app.route("/data",methods=["GET", "POST"])
def tellStory():
    result = {'username': 'gsh', 'password': 'gsh'}
    data = json.loads(request.data)
    print(data['time'])
    # time1 =float(request.form.get("time"))
    # print(time1)
    return Response(json.dumps(result), mimetype='application/json')

# 启动app
app.run(port=8081, host='0.0.0.0')
