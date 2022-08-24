#!/bin/python3
# 載入Flask套件
from flask import Flask,jsonify
from flask_restful import Api, Resource
from flask import render_template

'''--------------------------------------
    import api所提供的resouce file
---------------------------------------'''
from resource.index import test
from resource.User import User
from resource.Users import Users
from resource.login_handler import login_handler

app = Flask(__name__)
'''
加一個驗證
'''


'''
Api要提供的resource放在resource
'''
api = Api(app)
api.add_resource(test, "/")
api.add_resource(User, "/User/<string:id>")
api.add_resource(Users, "/Users")
api.add_resource(login_handler,"/api/login")
@app.route("/login")
def getLogin():
    return render_template("Logging.html")
if __name__ == "__main__":
    app.run(port=8087,debug=True)