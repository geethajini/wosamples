import random
import re
from typing import Dict, List
import uuid
from flask import Flask, request, render_template, send_file, jsonify, Response, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import requests
import json

import json

UPLOAD_FOLDER = 'templates'
ALLOWED_EXTENSIONS = set(['json'])
app = Flask(__name__)
CORS(app)

app.config[
    'MONGO_URI'] = 'mongodb://admin:admin@adapt-mongo-adapt.cp4ba-mission-16bf47a9dc965a843455de9f2aef2035-0000.eu-de.containers.appdomain.cloud:32535/LTI?authSource=admin'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)


@app.route('/api/swagger.json')
def swagger_json():
    # Read before use: http://flask.pocoo.org/docs/0.12/api/#flask.send_file
    return send_file('swagger.json')


SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={  # Swagger UI config overrides
    'app_name': "Add/update JD"
}, )

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/getUserDetailsUsingUserId', methods=['GET'])
def getUserDetailsUsingUserId():
    try:
        if request.method == 'GET':
            userId = request.args.get('userId')
            response = {"userId": "" + userId + "", "username": "John", "email": "JohnHCollin@gmail.com"}
        else:
            response = {"errorCode": "ER102",
                        "errorMessage": "Could not find the JRs"}
    except Exception as e:

        response = {"errorCode": "ER101",
                    "errorMessage": e}
    return response


@app.route('/getUserDetailsUsingName', methods=['GET'])
def getUserDetailsUsingName():
    try:
        if request.method == 'GET':
            userName = request.args.get('userName')
            print(userName)
            response = "123"
        else:
            response = {"errorCode": "ER102",
                        "errorMessage": "Could not find the JRs"}
    except Exception as e:

        response = {"errorCode": "ER101",
                    "errorMessage": e}
    return response


@app.route('/getAllUsers', methods=['GET'])
def getAllUsers():
    try:
        if request.method == 'GET':
            # userName = request.args.get('userName')
            #  print (userName)
            response = {"users": [{"userId": "123", "username": "John", "email": "JohnHCollin@gmail.com"},
                                  {"userId": "124", "username": "Rob", "email": "RobertBrauer@gmail.com"},
                                  {"userId": "125","username":"Anne","email":"AnneMaria@gmail.com"}]}
        else:
            response = {"errorCode": "ER102",
                        "errorMessage": "Could not find the JRs"}
    except Exception as e:

        response = {"errorCode": "ER101",
                    "errorMessage": e}
    return response

@app.route('/getUserIdFromUserDetails', methods=['GET'])
def getUserIdFromUserDetails():
    try:
        if request.method == 'GET':
            userDetails = request.get_json()
            #  print (userName)
            if userDetails is not None and "userId" in userDetails:
                response = userDetails["userId"]
            else:
                response="No JR Id Found"
        else:
            response = {"errorCode": "ER102",
                        "errorMessage": "Could not find the users"}
    except Exception as e:

        response = {"errorCode": "ER101",
                    "errorMessage": e}
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8081)
