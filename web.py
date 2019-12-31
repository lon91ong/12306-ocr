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
from config import listento
from ocr.ml_predict import Predict

class Resource(object):
    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        print('Path:', req.path)
        if req.path in ['/check-points', '/info.json']:
            resp.media = {"code":0,"Score":10000,"data":{"userPoints":10000, "availablePoints":8000, "lockPoints":2000}}
        elif req.path in ['/upload', '/check', '/create.json']:
            try:
                if req.path == '/upload': #联众API, for Bypass
                    img = b64decode(load(req.stream)['captchaData'])
                    # img = b64decode(loads(req.stream.read())['captchaData'])
                    result = Predict.share().get_coordinate(img, 'LianZ')
                    resp.body = dumps({"ts":2,"code":0, "data":{"recognition":result}})
                elif req.path =='/create.json': # ruokuai API
                    content = FieldStorage(fp=req.stream, environ=req.env) # falcon use cgi.FieldStorage parse form data
                    #softid = content.getvalue('soft_id')
                    img = content.getvalue('image') # attach image file in form data
                    img = img if type(img) is bytes else b64decode(img)
                    result = Predict.share().get_coordinate(img,'ZhuS')
                    resp.media = {"Result":result}
                else: # py12306 free
                    img = b64decode(load(req.stream)['img'])
                    result = Predict.share().get_coordinate(img)
                    resp.body = dumps({'msg': 'success', "result":result})
            except Exception as e:
                print("Error:",e.args[0])
                pass
        elif req.path in ['/report-error', '/reporterror.json']:
            resp.media = {"code":0,"Error":1,"data":{"result":True}}
        else:
            resp.media = {'code':1,'msg':'打码服务正常，访问姿势有误！'}
        resp.status = falcon.HTTP_200
    
    def on_get(self, req, resp):
        print("URL:", req.url)
        resp.media = {'code':1,'msg':'打码服务正常，访问姿势有误！'}
        resp.status = falcon.HTTP_200

class Web:
    def run(self, listenStr = listento):
        svrRes = Resource()
        app = falcon.API()
        apilst = ['/test','/info.json','/create.json','/reporterror.json','/check-points', '/upload', '/check', '/report-error']
        for apistr in apilst:
            app.add_route(apistr, svrRes)
        
        serve(app, listen = listenStr)

if __name__ == '__main__':
    Web().run('0.0.0.0:80')
