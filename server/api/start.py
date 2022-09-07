#!/bin/python3
# 載入Flask套件
from flask import Flask,jsonify, render_template,make_response, send_file
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

api = Api(app)

def verify_user_authorization_courses(userID):
    db=DBhandler()
    sql="SELECT authorization,course FROM `user` WHERE `userID`=\""+userID+"\""
    user_result=db.query(sql,True)
    if(len(user_result)==0):
        return None,None
    courses=user_result[0]["course"].split("/")
    return user_result[0]["authorization"],courses

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    print("token not authorization")
    return make_response(render_template("index.html",user="rrr"))


@app.route("/test")
def testUP():
    return render_template("test.html")

@app.route("/file/<string:userID>")
def download():
    return send_file("../file/user.csv", as_attachment=True) 

##登入頁面
@app.route("/")
def index():
    return render_template("index.html")

##遠端燒錄頁面
@app.route("/remote")
@jwt_required()
def remote():
    return render_template("remote.html")

##使用者選課程的頁面
@app.route("/course")
@jwt_required()
def course():
    jwt=JWT_handler()
    userID=jwt.readToken()["userID"]
    authorization,courses=verify_user_authorization_courses(userID)
    print(authorization)
    print(courses)
    return render_template("course.html",authorzation=authorization,courses=courses)

##使用者瀏覽某堂課程內容作業的頁面
@app.route("/course/<string:courseName>")
@jwt_required()
def homeworkbrowse(courseName):
    jwt=JWT_handler()
    db=DBhandler()
    userID=jwt.readToken()["userID"]
    authorization,courses=verify_user_authorization_courses(userID)
    if(courseName in courses):
        sql="SELECT homeworkName FROM "+courseName+"_HW "
        hw_result=db.query(sql,True)
        print(authorization)
        print(hw_result)
        return render_template("homeworkbrowse.html",authorzation=authorization,homeworks=hw_result)

##使用者看某項作業的詳細內容
@app.route("/course/<string:courseName>/<string:hwName>")
@jwt_required()
def homeworkcontent(courseName,hwName):
    jwt=JWT_handler()
    db=DBhandler()
    userID=jwt.readToken()["userID"]
    authorization,courses=verify_user_authorization_courses(userID)
    if(courseName in courses):
        sql="SELECT homeworkName,homeworkInfo,txtName,score,score2,score3 FROM "+courseName+"_HW  WHERE homeworkName=\""+hwName+"\""
        hw_result=db.query(sql,True)
        print(authorization)
        print(hw_result)
        return render_template("homeworkcontent.html",authorization=authorization,homework=hw_result)


##回傳遠端燒錄的檔案載點
@app.route("/file/<string:extension>")
@jwt_required()
def get_file(extension):
    jwt=JWT_handler()
    userID=jwt.readToken()["userID"]
    return send_file("../file/"+userID+"/"+userID+"."+extension, as_attachment=True)

##回傳特定作業的固定檔案的載點
@app.route("/staticFile/<string:courseName>/<string:hwName>/<string:fileName>")
@jwt_required()
def get_HWfile(courseName,hwName,fileName):
    return send_file("../file/"+courseName+"/"+hwName+"/"+fileName)

##回傳特定作業的非固定檔案的載點
@app.route("/activeFile/<string:courseName>/<string:hwName>/<string:fileName>")
@jwt_required()
def get_activeHWfile(courseName,hwName,fileName):
    jwt=JWT_handler()
    userID=jwt.readToken()["userID"]
    return send_file("../file/"+courseName+"/"+hwName+"/"+userID+"/"+fileName)

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