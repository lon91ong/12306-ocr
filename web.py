#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-13 14:24:03
# @Author  : lon91ong (lon91ong@gmail.com)
# @Link    : 
# @Version : $Id$

import falcon
from config import Config
from json import dumps,load
from waitress import serve
from base64 import b64decode
from ocr.ml_predict import Predict

class Resource(object):
    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        print('Path:', req.path)
        if req.path == '/check-points':
            resp.media = {"code":0,"message":"","data":{"userPoints":10000, "availablePoints":8000, "lockPoints":2000}}
        elif req.path == '/upload':
            try:
                img = b64decode(load(req.stream)['captchaData'])
            except Exception:
                pass
            result = Predict.share().get_coordinate(img,True)
            resp.body = dumps({"ts":2,"code":0,"message":"","data":{"recognition":result}})
        elif req.path == '/report-error':
            resp.media = {"code":0,"message":"","data":{"result":True}}
        resp.status = falcon.HTTP_200

class Web:
    def run(self):
        svrRes = Resource()
        app = falcon.API()
        app.add_route('/check-points', svrRes)
        app.add_route('/upload', svrRes)
        app.add_route('/report-error', svrRes)
        
        serve(app, listen = Config.WEB['host']+':'+str(Config.WEB['port']))

if __name__ == '__main__':
    Web().run()
