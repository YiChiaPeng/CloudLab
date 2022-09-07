from enum import unique
from flask_restful import Resource
from common.DBhandler import DBhandler
from flask_restful import reqparse
from common.JWT_handler import JWT_handler
from flask_jwt_extended import jwt_required

class course(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db=DBhandler()
        self.jwt=JWT_handler()

    @jwt_required()
    def post(self):
        user=self.jwt.readToken()
        self.sql="SELECT authorization,course,userID,userName FROM user where `userID` = \""+user['userID']+"\""
        user=self.db.query(self.sql,True)
        if user[0]["authorization"]=="1":
            parser = reqparse.RequestParser()
            parser.add_argument('courseName')
            arg=parser.parse_args()
            self.sql="SELECT * FROM courses where `courseName` = \""+arg['courseName']+"\""
            result=self.db.query(self.sql,True)
            if(len(result)==1):
                    return {
                        "success":"f",
                        "message":"the course name has been used"
                    }
            self.sql="INSERT INTO `courses`(`courseName`) VALUES (\"{}\")".format(arg['courseName'])
            self.db.query(self.sql,False)
            self.db.create_new_course_table(arg['courseName'])
            courses=user[0]["course"].split("/")
            courses.append(arg["courseName"])
            sql="UPDATE user SET course=\""+"/".join(courses)+"\" WHERE userID=\""+user[0]["userID"]+"\""
            self.db.query(sql,False)
            self.sql="INSERT INTO "+arg['courseName']+ " (`userID`,`userName`) VALUES (\"{}\",\"{}\")".format(user[0]["userID"],user[0]["userName"])
            self.db.query(self.sql,False)
            return {
                "success":"t",
                "message":"success!"
            }
        else:
            return {
                "success":"f",
                "message":"don't hava authorization"
            }
