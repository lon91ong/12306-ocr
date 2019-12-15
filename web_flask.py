from base64 import b64decode

from flask import Flask, jsonify, request
from config import Config
from json import loads
from ocr.ml_predict import Predict

app = Flask(__name__)


class Web:
    def run(self):
        app.run(**Config.WEB)

@app.route('/check-points', methods=['POST'], strict_slashes=False)
def check():
    return jsonify({"code":0,"message":"","data":{"userPoints":10000, "availablePoints":8000, "lockPoints":2000}})

@app.route('/report-error', methods=['POST'], strict_slashes=False)
def repErr():
    return jsonify({"code":0,"message":"","data":{"result":True}})

@app.route('/upload', methods=['POST'], strict_slashes=False)
def upload():
    try:
        img = b64decode(loads(str(request.stream.read(),encoding='utf-8'))['captchaData'])
    except Exception as e:
        print("error:",e.args[0])
        pass
    result = Predict.share().get_coordinate(img,True)
    return jsonify({"ts":2,"code":0,"message":"","data":{"recognition":result}})

if __name__ == '__main__':
    Web().run()
