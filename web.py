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
from cgi import FieldStorage
from ocr.ml_predict import Predict

class Resource(object):
    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        print('Path:', req.path)
        if req.path in ['/check-points', '/info.json']:
            resp.media = {"code":0,"Score":10000,"data":{"userPoints":10000, "availablePoints":8000, "lockPoints":2000}}
        elif req.path in ['/upload', '/create.json']:
            try:
                img = b64decode(load(req.stream)['captchaData']) if req.path == '/upload' \
                else FieldStorage(fp=req.stream, environ=req.env).getvalue('image')
            except Exception as e:
                print("error:",e.args[0])
                pass
            result = Predict.share().get_coordinate(img,req.path == '/upload')
            resp.body = dumps({"ts":2,"code":0,"Result":str(result)[1:-1],"data":{"recognition":result}})
        elif req.path in ['/report-error', '/reporterror.json']:
            resp.media = {"code":0,"Error":1,"data":{"result":True}}
        resp.status = falcon.HTTP_200

class Web:
    def run(self):
        svrRes = Resource()
        app = falcon.API()
        apilst = ['/info.json','/create.json','/reporterror.json','/check-points', '/upload', '/report-error']
        for apistr in apilst:
            app.add_route(apistr, svrRes)
        
        serve(app, listen = Config.WEB['host']+':'+str(Config.WEB['port']))

if __name__ == '__main__':
    Web().run()
