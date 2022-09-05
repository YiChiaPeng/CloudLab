from flask_restful import Resource
from common.DBhandler import DBhandler
from flask_restful import reqparse
from common.JWT_handler import JWT_handler
from flask_jwt_extended import jwt_required

class homework(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db=DBhandler()
        self.jwt=JWT_handler()


    @jwt_required()
    def get(self):
        user=self.jwt.readToken()
        userID=user['userID']
        parser = reqparse.RequestParser()
        parser.add_argument('courseName')
        parser.add_argument('homeworkName')
        arg=parser.parse_args()
        self.sql="SELECT course FROM user where `userID` = \""+userID+"\"" 
        result=self.db.query(self.sql,True)
        result=result.split("/")
        if(arg["courseName"] in result):
            self.sql="SELECT homeworkInfo FROM "+arg["courseName"]+"_HW where homeworkName="+arg["homeworkName"] 
            info=self.db.query(self.sql,True)
            self.sql="SELECT "+arg["homeworkName+"]+" FROM "+arg["courseName"]
            score=self.db.query(self.sql,True)
            return{
                "info":info[0]["homeworkInfo"],
                "score":score[0][arg["homeworkName"]]
            }
        else:
            return{
                "message":"you dont have authorization"
            },
