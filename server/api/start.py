#!/bin/python3
# 載入Flask套件
from flask import Flask,jsonify, render_template,make_response
from flask_restful import Api
from common.JWT_handler import JWT_handler
from common.DBhandler import DBhandler
from flask_jwt_extended import  JWTManager,jwt_required
'''--------------------------------------
    import api所提供的resouce file
---------------------------------------'''
from resource.User import User
from resource.Users import Users
from resource.login_handler import login_handler
from resource.ProgrammingRequest import ProgrammingRequest
from resource.course import course
from resource.homework import homework
from resource.homeworks import homeworks
from resource.ProgrammingTest_without_hardware import ProgrammingTest_without_hardware


app = Flask(__name__)
jwt=JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'test' 
app.config['JWT_TOKEN_LOCATION']=['headers','cookies']
app.config['JWT_ACCESS_COOKIE_NAME']="access_token_cookie"
app.config['JWT_ACCESS_TOKEN_EXPIRES']=3600

'''
Api要提供的resource放在resource
'''


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return make_response(render_template("index.html",user="rrr"))


api = Api(app)

@app.route("/test")
def testUP():
    return render_template("test.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remote")
@jwt_required()
def remote():
    return render_template("remote.html")

@app.route("/course")
@jwt_required()
def course():
    jwt=JWT_handler()
    db=DBhandler()
    userID=jwt.readToken()["userID"]
    sql="SELECT authorization,course FROM `user` WHERE `userID`=\""+userID+"\""
    user_result=db.query(sql,True)
    if(len(user_result)==0):
        return {
            "message":"you can't do this"
        }
    courses=user_result[0]["course"].split("/")
    return render_template("enterclass.html",authorzation=user_result[0]["authorization"],courses=courses)

@app.route("/homeworkbrowse")
@jwt_required()
def homeworkbrowse():
    return render_template("homeworkbrowse.html")

@app.route("/homeworkcontent")
@jwt_required()
def homeworkcontent():
    return render_template("homeworkcontent.html")

api.add_resource(User, "/api/User")
api.add_resource(Users, "/api/Users")
api.add_resource(login_handler,"/api/login")
##api.add_resource(ProgrammingRequest,"/api/ProgrammingRequest")
##api.add_resource(course,"/api/course")
api.add_resource(homework,"/api/homework")
api.add_resource(homeworks,"/api/homeworks")
api.add_resource(ProgrammingTest_without_hardware,"/api/ProgrammingRequest")

if __name__ == "__main__":
    app.run(port=8087,debug=True)