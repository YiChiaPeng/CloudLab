from flask import Flask,jsonify
from flask_restful import Api
#驗證登錄
from flask_httpauth import HTTPBasicAuth


'''--------------------------------------
    import api所提供的resouce file
---------------------------------------'''
from resource.User import User
from resource.index import test


app = Flask(__name__)
'''
加一個驗證
'''
auth = HTTPBasicAuth()


'''
Api要提供的resource放在resource
'''
api = Api(app)
api.add_resource(test, "/")
api.add_resource(User, "/user")
if __name__ == "__main__":
    app.run()