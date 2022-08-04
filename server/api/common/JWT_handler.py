from base64 import encode
from hashlib import algorithms_available
import jwt
import json

class JWT_handler():
    def makeToken(self,data):
        return jwt.encode(data,"test",algorithm="HS256")
    def readToken(self,token):
        return jwt.decode(token)