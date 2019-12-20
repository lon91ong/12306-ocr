#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-13 14:24:03
# @Author  : lon91ong (lon91ong@gmail.com)
# @Link    : 
# @Version : $Id$

import falcon
from json import dumps,load,loads
from waitress import serve
from base64 import b64decode
from cgi import FieldStorage
from config.Config import WEB as HoP
from ocr.ml_predict import Predict

class Resource(object):
    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        print('Path:', req.path)
        if req.path in ['/check-points', '/info.json']:
            resp.media = {"code":0,"Score":10000,"data":{"userPoints":10000, "availablePoints":8000, "lockPoints":2000}}
        elif req.path in ['/upload', '/check', '/create.json',]:
            try:
                img = b64decode(load(req.stream)['captchaData']) if req.path == '/upload' \
                else b64decode(loads(str(req.stream.read(),encoding='utf-8'))['img']) if req.path == '/check' \
                else FieldStorage(fp=req.stream, environ=req.env).getvalue('image')
                print(img)
            except Exception as e:
                print("error:",e.args[0])
                pass
            result = Predict.share().get_coordinate(img,req.path == '/upload')
            print(result)
            resp.body = dumps({'msg': 'success', 'result': result}) if req.path == '/check' \
            else dumps({"ts":2,"code":0,"Result":str(result)[1:-1],"data":{"recognition":result}})
        elif req.path in ['/report-error', '/reporterror.json']:
            resp.media = {"code":0,"Error":1,"data":{"result":True}}
        resp.status = falcon.HTTP_200

class Web:
    def run(self, listenStr=HoP['host']+':'+str(HoP['port'])):
        svrRes = Resource()
        app = falcon.API()
        apilst = ['/info.json','/create.json','/reporterror.json','/check-points', '/upload', '/report-error']
        for apistr in apilst:
            app.add_route(apistr, svrRes)
        
        serve(app, listen = listenStr)

if __name__ == '__main__':
    Web().run('0.0.0.0:80')
