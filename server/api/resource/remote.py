import os
from flask import Flask, request, redirect, url_for
from flask_restful import Resource
from werkzeug.utils import secure_filename

class remote(Resource):
    def post(self):
        if request.method == 'POST':
            file = request.files['file']
            if(file):
                
                file.save("../file/test.sql")
                return 0
            else:
                return 1
            