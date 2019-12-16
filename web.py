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
        if req.path == '/check-points' or req.path == '/info.json':
            resp.media = {"code":0,"Score":10000,"data":{"userPoints":10000, "availablePoints":8000, "lockPoints":2000}}
        elif req.path == '/upload' or req.path == '/create.json':
            try:
                img = b64decode(load(req.stream)['captchaData']) if req.path == '/upload' \
                else req.media.get('username')
                #print(img)
            except Exception as e:
                print("error:",e.args[0])
                pass
            result = Predict.share().get_coordinate(img,True)
            resp.body = dumps({"ts":2,"code":0,"Result":result.replace('|',','),"data":{"recognition":result}})
        elif req.path == '/report-error' or req.path == '/reporterror.json':
            resp.media = {"code":0,"Error":1,"data":{"result":True}}
        resp.status = falcon.HTTP_200

class Web:
    def run(self):
        svrRes = Resource()
        app = falcon.API()
        app.add_route('/info.json', svrRes)
        app.add_route('/create.json', svrRes)
        app.add_route('/reporterror.json', svrRes)
        app.add_route('/check-points', svrRes)
        app.add_route('/upload', svrRes)
        app.add_route('/report-error', svrRes)
        
        serve(app, listen = Config.WEB['host']+':'+str(Config.WEB['port']))

if __name__ == '__main__':
    Web().run()
