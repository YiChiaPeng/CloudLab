#!/bin/python3
# 載入Flask套件
from flask import Flask,jsonify
from flask_restful import Api, Resource


'''--------------------------------------
    import api所提供的resouce file
---------------------------------------'''
from resource.index import test
from resource.User import User
from resource.Users import Users

app = Flask(__name__)
'''
加一個驗證
'''


'''
Api要提供的resource放在resource
'''
'''
string	文字類型(默認類型)
int	整數
float	浮點數
path	跟 string 差不多，但可以有斜線 /
uuid	UUID 字符串
'''
api = Api(app)
api.add_resource(test, "/")
api.add_resource(User, "/User/<string:id>")
api.add_resource(Users, "/Users")
if __name__ == "__main__":
    app.run(port=8087,debug=True)