from flask import Flask
from flask_restful import Api
from resource.index import test

app = Flask(__name__)
api = Api(app)

api.add_resource(test, "/")

if __name__ == "__main__":
    app.run()