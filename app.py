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

app.config['MONGO_URI'] = 'mongodb://admin:admin@adapt-mongo-adapt.cp4ba-mission-16bf47a9dc965a843455de9f2aef2035-0000.eu-de.containers.appdomain.cloud:32535/LTI?authSource=admin'
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
},)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@app.route('/getAllJobRequisitions', methods=['GET'])
def get_all_job_requisitions():
    if request.method == 'GET':
        department = request.args.get('department')
        jobProfile = request.args.get('jobProfile')
        location = request.args.get('location')
        status = request.args.get('status')

        try:
            # The below line of code is used to extract JRs inside instances field. Now we don't have instances field in Mongo DB
            # We have each JR as an individual document in MOngo DB collection so below query is not needed.
            # jrs = mongo.db.WORecruitmentFlow.find({}, {"instances": 0, "_id": 0})
            jrs = mongo.db.WORecruitmentFlow.find(
                {"jobReqId": {"$exists": True}}, {"_id": 0})
            jrs_string = dumps(jrs)
            # response = jrs
            print("Jrs from Mongo db ==== " + jrs_string)
            print(type(jrs_string))
            print(type(jrs))
            jrs_response = []
            if None not in (department, location, jobProfile, status):
                print('Query string department = ' + department)
                print('Query string location = ' + location)
                print('Query string status = ' + status)
                print('Query string jobProfile = ' + jobProfile)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if ("city" in i or "country" in i or "state" in i or "location" in i) and "department" in i and "status" in i and "jobProfile" in i:
                        _city = i["city"].lower()
                        _country = i["country"].lower()
                        _state = i["state"].lower()
                        _department = i["department"].lower()
                        _location = i["location"].lower()
                        _status = i["status"].lower()
                        _jobProfile = i["jobProfile"].lower()
                        if (((_city is not None and _city and location.lower() in _city)
                            or (_country is not None and _country and location.lower() in _country)
                                or (_state is not None and _state and location.lower() in _state)
                             or (_location is not None and _location and location.lower() in _location))
                            and (_department is not None and _department and department.lower() in _department)
                                and (_status is not None and _status and status.lower() in _status)
                                and (_jobProfile is not None and _jobProfile and jobProfile.lower() in _jobProfile)):
                            print("_city" + _city)
                            print("_country" + _country)
                            print("_state" + _state)
                            print("_location" + _location)
                            print("_department" + _department)
                            print("_status" + _status)
                            print("_jobProfile" + _jobProfile)
                            jrs_response.append(i)
            elif None not in (location, status):
                print('Query string status = ' + status)
                print('Query string location = ' + location)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if ("city" in i or "country" in i or "state" in i or "location" in i) and "status" in i:
                        _city = i["city"].lower()
                        _country = i["country"].lower()
                        _state = i["state"].lower()
                        _location = i["location"].lower()
                        _status = i["status"].lower()
                        if (((_city is not None and _city and location.lower() in _city)
                            or (_country is not None and _country and location.lower() in _country)
                                or (_state is not None and _state and location.lower() in _state)
                             or (_location is not None and _location and location.lower() in _location))
                                and (_status is not None and _status and status.lower() in _status)):
                            print("_city" + _city)
                            print("_country" + _country)
                            print("_state" + _state)
                            print("_location" + _location)
                            print("_status" + _status)
                            jrs_response.append(i)
            elif None not in (department, status):
                print('Query string department = ' + department)
                print('Query string location = ' + location)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if "department" in i and "status" in i:
                        _department = i["department"].lower()
                        _status = i["status"].lower()
                        if ((_department is not None and _department and department.lower() in _department)
                                and (_status is not None and _status and status.lower() in _status)):
                            print("_department" + _department)
                            print("_status" + _status)
                            jrs_response.append(i)
            elif None not in (location, department):
                print('Query string department = ' + department)
                print('Query string location = ' + location)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if ("city" in i or "country" in i or "state" in i or "location" in i) and "department" in i:
                        _city = i["city"].lower()
                        _country = i["country"].lower()
                        _state = i["state"].lower()
                        _location = i["location"].lower()
                        _department = i["department"].lower()
                        if (((_city is not None and _city and location.lower() in _city)
                            or (_country is not None and _country and location.lower() in _country)
                                or (_state is not None and _state and location.lower() in _state)
                             or (_location is not None and _location and location.lower() in _location))
                                and (_department is not None and _department and department.lower() in _department)):
                            print("_city" + _city)
                            print("_country" + _country)
                            print("_state" + _state)
                            print("_location" + _location)
                            print("_department" + _department)
                            jrs_response.append(i)
            elif None not in (location, jobProfile):
                print('Query string location = ' + location)
                print('Query string jobProfile = ' + jobProfile)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if ("city" in i or "country" in i or "state" in i or "location" in i) and "jobProfile" in i:
                        _city = i["city"].lower()
                        _country = i["country"].lower()
                        _state = i["state"].lower()
                        _location = i["location"].lower()
                        _jobProfile = i["jobProfile"].lower()
                        if (((_city is not None and _city and location.lower() in _city)
                            or (_country is not None and _country and location.lower() in _country)
                                or (_state is not None and _state and location.lower() in _state)
                             or (_location is not None and _location and location.lower() in _location))
                                and (_jobProfile is not None and _jobProfile and jobProfile.lower() in _jobProfile)):
                            print("_city" + _city)
                            print("_country" + _country)
                            print("_state" + _state)
                            print("_jobProfile" + _jobProfile)
                            jrs_response.append(i)
            elif None not in (jobProfile, department):
                print('Query string department = ' + department)
                print('Query string jobProfile = ' + jobProfile)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if "jobProfile" in i and "department" in i:
                        _jobProfile = i["jobProfile"].lower()
                        _department = i["department"].lower()
                        if ((_jobProfile is not None and _jobProfile and jobProfile.lower() in _jobProfile)
                                and (_department is not None and _department and department.lower() in _department)):
                            print("_jobProfile" + _jobProfile)
                            print("_department" + _department)
                            jrs_response.append(i)
            elif department is not None:
                print('Query string department = ' + department)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if "department" in i:
                        _department = i["department"].lower()
                        if ((_department is not None and _department and department.lower() in _department)):
                            print("_department" + _department)
                            jrs_response.append(i)
            elif jobProfile is not None:
                print('Query string jobProfile = ' + jobProfile)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if "jobProfile" in i:
                        _jobProfile = i["jobProfile"].lower()
                        if ((_jobProfile is not None and _jobProfile and jobProfile.lower() in _jobProfile)):
                            print("_jobProfile" + _jobProfile)
                            jrs_response.append(i)
            elif location is not None:
                print('Query string location = ' + location)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if ("city" in i or "country" in i or "state" in i or "location" in i):
                        _city = i["city"].lower()
                        _country = i["country"].lower()
                        _state = i["state"].lower()
                        _location = i["location"].lower()
                        _status = i["status"].lower()
                        if (((_city is not None and _city and location.lower() in _city)
                            or (_country is not None and _country and location.lower() in _country)
                                or (_state is not None and _state and location.lower() in _state)
                             or (_location is not None and _location and location.lower() in _location))):
                            print("_city" + _city)
                            print("_country" + _country)
                            print("_state" + _state)
                            print("_location" + _location)
                            print("_status" + _status)
                            jrs_response.append(i)
            elif status is not None:
                print('Query string status = ' + status)
                jrs_json = json.loads(jrs_string)
                # print('type(jrs_json = ' + str(type(jrs_json)))
                for i in jrs_json:
                    if "status" in i:
                        _status = i["status"].lower()
                        if ((_status is not None and _status and status.lower() in _status)):
                            print("_status" + _status)
                            jrs_response.append(i)

            if not jrs_response and jrs_string:
                jrs_response = json.loads(jrs_string)
                response = {}
                response['instances'] = jrs_response
                print("response - if " + str(response))
                return response
            elif jrs_response:
                # jrs_response_json = jsonify(jrs_response)
                response = {}
                response['instances'] = jrs_response
                print("response - else " + str(response))
                return response
            else:
                response = {"errorCode": "ER102",
                            "errorMessage": "Could not find the JRs"}
                return response

        except Exception as e:

            response = {"errorCode": "ER101",
                        "errorMessage": e}
            return response


@app.route('/createNewEmptyJobRequisition', methods=['POST'])
def create_new_empty_job_requisition():
    if request.method == 'POST':
        response = {}
        #existing_jr = request.get_json()
        #print("type(existing_jr) = " + str(type(existing_jr)))
        # print("---existing_jr---")
        # print(existing_jr)
        new_jr = {
            "jobReqId": "",
            "jobStartDate": "",
            "department": "",
            "division": "",
            "location": "",
            "costOfHire": "",
            "country": "",
            "createdDateTime": "",
            "currency": "",
            "salRateType": "",
            "salaryBase": "",
            "candidateProgress": "",
            "city": "",
            "state": "",
            "closedDateTime": "",
            "status": "",
            "jobDescription": "",
            "hiringManager": "",
            "hiringManagerNote": "",
            "jobProfile": "",
            "workExperience": "",
            "recruiter": "",
            "competency_type": "",
            "competency_description": "",
            "competency_id": ""
        }

        print("---new_jr----- BEFORE ----")
        print(new_jr)
        print("type(new_jr) = " + str(type(new_jr)))
        new_jrID = ""
        if new_jr is not None:
            new_jrID = "JR" + str(random.randint(1000, 9999))
            print("new jr id = " + new_jrID)
            new_jr["jobReqId"] = new_jrID
            print("---new_jr----- AFTER ----")
            print(new_jr)
            jrs = mongo.db.WORecruitmentFlow.insert_one(new_jr)
            print("---jrs_withoutid----- AFTER ----")
            jrs_withoutid = mongo.db.WORecruitmentFlow.find_one(
                {"jobReqId": new_jrID}, {"_id": 0})
            print(jrs_withoutid)
            jrs_withoutid_string = dumps(jrs_withoutid)
            jrs_withoutid_json = json.loads(jrs_withoutid_string)
            print(jrs_withoutid_json)
            response["Job_Requisition"] = (jrs_withoutid_json)
            response["jobReqId"] = (new_jrID)
            response_string = json.dumps(response, default=str)
            response_json = json.loads(response_string)
            #return response
            return response_json
        else:
            response["message"] = "Error in adding new JR"
            return response


@app.route('/createNewJobRequisition', methods=['POST'])
def create_new_job_requisition():
    if request.method == 'POST':
        response = {}
        existing_jr = request.get_json()
        print("type(existing_jr) = " + str(type(existing_jr)))
        print("---existing_jr---")
        print(existing_jr)
        new_jr = existing_jr["job_requisitions"]
        print("---new_jr----- BEFORE ----")
        print(new_jr)
        print("type(new_jr) = " + str(type(new_jr)))
        new_jrID = ""
        if existing_jr is not None and "job_requisitions" in existing_jr and "jobReqId" in existing_jr["job_requisitions"]:
            existing_jrID = existing_jr["job_requisitions"]["jobReqId"]
            lastExistingJR = mongo.db.WORecruitmentFlow.find_one(
                {}, sort=[('jobReqId', -1)])
            if existing_jrID or lastExistingJR is not None:
                lastExistingJRId = lastExistingJR["jobReqId"]
                existing_JRId = ""
                if lastExistingJRId:
                    existing_JRId = lastExistingJRId
                else:
                    existing_JRId = existing_jrID
                print("existing_JRId[-4:] = " + existing_JRId[-4:])
                last_four_chars = existing_JRId[-4:]
                print(last_four_chars.isnumeric())
                if (last_four_chars and last_four_chars.isnumeric()):
                    new_jrID = f'{"JR"}{int(last_four_chars)+1:04d}'
                if not new_jrID:
                    new_jrID = "JR" + str(random.randint(1000, 9999))
                print("new jr id = " + new_jrID)
            else:
                new_jrID = "JR" + str(random.randint(1000, 9999))
            new_jr["jobReqId"] = new_jrID
            jrs = mongo.db.WORecruitmentFlow.insert_one(new_jr)
        if new_jr is not None:
            #response["message"] = "Added new Job requisition with ID = " + new_jrID
            #response = json.dumps(new_jr, indent = 4)
            # print(new_jr)
            #response = jsonify(new_jr)
            #jrs_json = dumps(jrs)
            #response = json.loads(jrs_json)
            #response["message"] = "New JR created!!! New JR ID is : " + new_jrID
            print("---jrs_withoutid----- AFTER ----")
            jrs_withoutid = mongo.db.WORecruitmentFlow.find_one(
                {"jobReqId": new_jrID}, {"_id": 0})
            print(jrs_withoutid)
            jrs_withoutid_string = dumps(jrs_withoutid)
            jrs_withoutid_json = json.loads(jrs_withoutid_string)
            response["Job_Requisition"] = jrs_withoutid_json
            response["jobReqId"] = new_jrID


            response_string = json.dumps(response, default=str)
            response_json = json.loads(response_string)
            print(response_json)
            return response_json
            #return response
        else:
            response["message"] = "Error in adding new JR"
            return response


@app.route('/getJobRequisition', methods=['GET'])
def get_job_requisition():
    if request.method == 'GET':
        input_JRId = request.args.get('JRId')
        response = {}
        print("type(input_JRId) = " + str(type(input_JRId)))
        print("---input_JRId---")
        print(input_JRId)
        if input_JRId is not None :
           # existing_jrID = existing_jr["job_requisitions"]["jobReqId"]
            lastExistingJR = mongo.db.WORecruitmentFlow.find_one(
                {}, sort=[('jobReqId', -1)])

            print(lastExistingJR)
            if lastExistingJR is not None:
                ExistingJR_String=dumps(lastExistingJR)
                Job_Requisition_JSON = {"Job_Requisition": lastExistingJR}
                print(Job_Requisition_JSON)
                json_dumps = json.dumps(Job_Requisition_JSON, default=str)
                response = json.loads(json_dumps)
               # response=json.loads(ExistingJR_String)
                return response
            else:
                response["message"] = "JR" + input_JRId+" not found."
                return response
                """
                lastExistingJRId = lastExistingJR["jobReqId"]
                existing_JRId = ""
                if lastExistingJRId:
                    existing_JRId = lastExistingJRId
                else:
                    existing_JRId = existing_jrID
                print("existing_JRId[-4:] = " + existing_JRId[-4:])
                last_four_chars = existing_JRId[-4:]
                print(last_four_chars.isnumeric())
                if (last_four_chars and last_four_chars.isnumeric()):
                    new_jrID = f'{"JR"}{int(last_four_chars)+1:04d}'
                if not new_jrID:
                    new_jrID = "JR" + str(random.randint(1000, 9999))
                print("new jr id = " + new_jrID)

        if new_jr is not None:
            #response["message"] = "Added new Job requisition with ID = " + new_jrID
            #response = json.dumps(new_jr, indent = 4)
            # print(new_jr)
            #response = jsonify(new_jr)
            #jrs_json = dumps(jrs)
            #response = json.loads(jrs_json)
            #response["message"] = "New JR created!!! New JR ID is : " + new_jrID
            print("---jrs_withoutid----- AFTER ----")
            jrs_withoutid = mongo.db.WORecruitmentFlow.find_one(
                {"jobReqId": new_jrID}, {"_id": 0})
            print(jrs_withoutid)
            jrs_withoutid_string = dumps(jrs_withoutid)
            jrs_withoutid_json = json.loads(jrs_withoutid_string)
            response["Job_Requisition"] = jrs_withoutid_json
            response["jobReqId"] = new_jrID


            response_string = json.dumps(response, default=str)
            response_json = json.loads(response_string)
            print(response_json)
            return response_json
            #return response
        else:
            response["message"] = "Error in adding new JR"
            return response
"""

@app.route('/workOnExistingRequisition', methods=['POST'])
def work_on_exisiting_Requisition():
    if request.method == 'POST':
        input_json = request.get_json()
        response = input_json['job_requisitions']
        response = {'Job_Requisition': response}
        return response


@app.route('/getJRId', methods=['GET'])
def getJRIds():
    if request.method == 'GET':
        existing_jr = request.get_json()
        response = {}
        if existing_jr is not None and "jobReqId" in existing_jr:
            response["jobReqId"] = existing_jr["jobReqId"]
        else:
            response["message"] = "No JR ID found"
        return response


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/modifyJobDescription', methods=['POST'])
def update_JD():
    if request.method == 'POST':
        job_description = request.args.get('JOBDescription')
        jobReqId = request.args.get('jobReqId')
        print(jobReqId)
        Job_Requisition = mongo.db.WORecruitmentFlow.find_one(
            {"jobReqId": jobReqId}, {"_id": 0})
        print(Job_Requisition)
        #Job_Requisition = request.get_json();
        print(Job_Requisition)
        Job_Requisition['jobReqLocale'][0]['jobDescription'] = job_description
        mongo.db.WORecruitmentFlow.update_one(
            {"jobReqId": Job_Requisition['jobReqId']}, {"$set": Job_Requisition})
        Job_Requisition_JSON = {"Job_Requisition": Job_Requisition}
        print(Job_Requisition_JSON)
        json_dumps = json.dumps(Job_Requisition_JSON, default=str)
        response = json.loads(json_dumps)
        return response


@app.route('/modifyCompetency', methods=['POST'])
def update_Competency():
    if request.method == 'POST':
        input_josn = request.get_json()
        print(input_josn)
        Job_Requisition = input_josn['Job_Requisition']
        competency = input_josn['competency']
        print(competency)
        Job_Requisition['competency'] = competency
        print(Job_Requisition)
        mongo.db.WORecruitmentFlow.update_one(
            {"jobReqId": Job_Requisition['jobReqId']}, {"$set": Job_Requisition})
        Job_Requisition_JSON = {"Job_Requisition": Job_Requisition}
        print(Job_Requisition_JSON)
        json_dumps = json.dumps(Job_Requisition_JSON, default=str)
        response = json.loads(json_dumps)
        return response


@app.route('/getInterViewwrs', methods=['GET'])
def get_interviewers():
    if request.method == 'GET':
        Interviewers = {"instances": [
            {
                "interviewer_name": "john",
                "interviewer_id": "IIDS1223a",
                "interviewer_designation": "Architect",
                "jobReqId": "JR1234"
            },
            {
                "interviewer_name": "jade",
                "interviewer_id": "IIDS6670o",
                "interviewer_designation": "Architect",
                "jobReqId": "JR1235"
            },
            {
                "interviewer_name": "oliver",
                "interviewer_id": "IIDS4433L",
                "interviewer_designation": "Architect",
                "jobReqId": "JR1236"
            },
            {
                "interviewer_name": "gracie",
                "interviewer_id": "IIDS5547M",
                "interviewer_designation": "Architect",
                "jobReqId": "JR1237"
            }
        ]
        }
        print(Interviewers)
        return jsonify(Interviewers)


@app.route('/getChannelNames', methods=['GET'])
def get_Channels():
    if request.method == 'GET':
        ChannelList = {"instances": [
            {
                "channelName": "Monster"
            },
            {
                "channelName": "Indeed"
            },
            {
                "channelName": "Dice"
            },
            {
                "channelName": "CareerBuilder"
            },
            {
                "channelName": "Linkedin"
            },
            {
                "channelName": "Kube Careers"
            },
            {
                "channelName": "Ziprecruiter"
            },
            {
                "channelName": "simplyhired"
            },
            {
                "channelName": "Ziprecruiter"
            },
            {
                "channelName": "Newyork Jobs"
            },
            {
                "channelName": "Behance"
            },
            {
                "channelName": "Dribbble"
            },
            {
                "channelName": "Carbonmade"
            },
            {
                "channelName": "Coroflot"
            },
            {
                "channelName": "SalesHeads.com"
            },
            {
                "channelName": "SalesJobs.com"
            },
            {
                "channelName": "Sales Gravy"
            }
        ]
        }
        print(ChannelList)
        return jsonify(ChannelList)


@app.route('/getSourcers', methods=['GET'])
def get_sourcers():
    if request.method == 'GET':
        Sourcers = {"instances": [
            {
                "email": "eva.marie@abc.com",
                "firstName": "eva",
                "jobReqId": "JR1234",
                "lastName": "marie",
                "phone": "1908877535"
            },
            {
                "email": "seba.kenny@abc.com",
                "firstName": "seba",
                "jobReqId": "JR1235",
                "lastName": "kenny",
                "phone": "0986544553"
            },
            {
                "email": "stefan.rose@abc.com",
                "firstName": "stefan",
                "jobReqId": "JR1236",
                "lastName": "rose",
                "phone": "9987654456"
            },
            {
                "email": "andrew.ben@abc.com",
                "firstName": "andrew",
                "jobReqId": "JR1237",
                "lastName": "ben",
                "phone": "9877665549"
            }
        ]
        }
        print(Sourcers)
        return jsonify(Sourcers)


@app.route('/getRecruiters', methods=['GET'])
def get_recruiters():
    if request.method == 'GET':
        Recruiters = {"instances": [
            {
                "email": "mary.green@abc.com",
                "firstName": "Mary",
                "jobReqId": "JR1234",
                "lastName": "Green",
                "phone": "1198254276"
            },
            {
                "email": "julia.roberts@abc.com",
                "firstName": "Julia",
                "jobReqId": "JR1235",
                "lastName": "Roberts",
                "phone": "9988764532"
            },
            {
                "email": "david.roberts@abc.com",
                "firstName": "David",
                "jobReqId": "JR1236",
                "lastName": "Roberts",
                "phone": "8877654309"
            },
            {
                "email": "laura.beth@abc.com",
                "firstName": "Laura",
                "jobReqId": "JR1237",
                "lastName": "Beth",
                "phone": "7866554834"
            }
        ]
        }
        print(Recruiters)
        return jsonify(Recruiters)


@app.route('/modifyInterviewers', methods=['POST'])
def update_Interviewers():
    if request.method == 'POST':

        inputJson = request.get_json()
        Job_Requisition = inputJson['Job_Requisition']
        interviewer_assigned = inputJson['interviewers_filter_list']
        print(Job_Requisition)
        Job_Requisition['interviewers'] = interviewer_assigned
        sourcer_len = len(Job_Requisition['interviewers'])

        # i=0;
        # for interviewer in interviewer_assigned:
        # if(sourcer_len<):
        #Job_Requisition['interviewers'][i] = interviewer;
        # else:
        # Job_Requisition['interviewers'].append(interviewer)

        #i +=1;

        #Job_Requisition['interviewers'][0] = InterViewer1;
        #Job_Requisition['interviewers'][0] = InterViewer2;

        mongo.db.WORecruitmentFlow.update_one(
            {"jobReqId": Job_Requisition['jobReqId']}, {"$set": Job_Requisition})
        Job_Requisition_JSON = {"Job_Requisition": Job_Requisition}
        print(Job_Requisition_JSON)
        json_dumps = json.dumps(Job_Requisition_JSON, default=str)
        response = json.loads(json_dumps)
        return response


@app.route('/modifySourcer', methods=['POST'])
def update_Sourcer():
    if request.method == 'POST':
        inputJson = request.get_json()
        Job_Requisition = inputJson['Job_Requisition']
        sourcers_assigned = inputJson['sourcers_filter_list']
        print(Job_Requisition)
        Job_Requisition['sourcers'] = sourcers_assigned
        print(Job_Requisition)
        mongo.db.WORecruitmentFlow.update_one(
            {"jobReqId": Job_Requisition['jobReqId']}, {"$set": Job_Requisition})
        Job_Requisition_JSON = {"Job_Requisition": Job_Requisition}
        print(Job_Requisition_JSON)
        json_dumps = json.dumps(Job_Requisition_JSON, default=str)
        response = json.loads(json_dumps)
        return response


@app.route('/modifyRecruiter', methods=['POST'])
def update_Recruiter():
    if request.method == 'POST':
        inputJson = request.get_json()
        Job_Requisition = inputJson['Job_Requisition']
        recruiters_assigned = inputJson['recruiters_filter_list']
        print(Job_Requisition)
        Job_Requisition['recruiters'] = recruiters_assigned
        print(Job_Requisition)
        mongo.db.WORecruitmentFlow.update_one(
            {"jobReqId": Job_Requisition['jobReqId']}, {"$set": Job_Requisition})
        Job_Requisition_JSON = {"Job_Requisition": Job_Requisition}
        print(Job_Requisition_JSON)
        json_dumps = json.dumps(Job_Requisition_JSON, default=str)
        response = json.loads(json_dumps)
        return response


@app.route('/postJOBRequisition', methods=['POST'])
def post_job():
    if request.method == 'POST':
        jobReqId = request.args.get("jobReqId")
        jobProfile = request.args.get("jobProfile")
        channelName = request.args.get("channelName")
        #print(jobReqId + " " + jobProfile + " " + channelName)

        jrs_withoutid = mongo.db.WORecruitmentFlow.find_one(
                {"jobReqId": jobReqId}, {"_id": 0})
        print("post job jrs_withoutid = " + str(jrs_withoutid))
        jrs_withoutid_string = dumps(jrs_withoutid)
        jrs_withoutid_json = json.loads(jrs_withoutid_string)
        jobDesc = jrs_withoutid_json["jobDescription"]
        response_json = {}

        if channelName is not None :
            if channelName == "Linked In" or channelName == "LinkedIn": 
                print("inside if channelName " + channelName)
                url = "https://api.linkedin.com/v2/ugcPosts"

                payload = json.dumps({
                "author": "urn:li:person:Ayyquo2cKD",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": jobDesc + " \n Please send email to 'jobs@woacmecorp.com' for further details."
                    },
                    "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
                }
                })
                headers = {
                'Authorization': 'Bearer AQWRfu3AN9G8-xnxk3cY0JaTTdc4iO-7WUKLl4upLkwcRwckfqvQ9Lw1hrcBYVZpRnQDvVmPiCSLJclDdvj9qoEMZbxloZ8UtEbmx090gltvOkFqhWhd1cp1QODXlfxNF-n9ABCFFlPQ7uQwALKUsRepj6Q87l8_uc5cUmhbqFEz3djX-lHqtmoEB4FVa4SBZ_JFiBDvParG316JaUlZGmwTwHBOk2N_zA4ceQeOcTrdXy7WUmMbXd2Vd7AzKF0Oqtl_Ws_RKwd28HnAbnKKsarzrnidjqZYPIcedK7U_XwMP6xMLxrk9YzbIpLXU8baWbRAuTPUSiwPThycM5cuuaBL48uNcw',
                'Content-Type': 'application/json',
                'Cookie': 'lidc="b=VB51:s=V:r=V:a=V:p=V:g=3284:u=4:x=1:i=1671642348:t=1671646515:v=2:sig=AQHVEdai1Q7Lj8Q0N3KQa7lXThuRe94y"; bcookie="v=2&f4a53cc3-9f87-47d7-8a78-cf544bcd2e41"; lang=v=2&lang=en-us; lidc="b=VB51:s=V:r=V:a=V:p=V:g=3284:u=4:x=1:i=1671642243:t=1671642915:v=2:sig=AQHvcQ2xL0pmGu5QzgdkFrF8rt1CBDV8"'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)

                response_text = "Job posted in LinkedIn. \n Please check this url to view the job posting : https://www.linkedin.com/in/test-account-wo-acme-corp-a9b34725b/recent-activity/"

                response_json["response"] = response_text

                return response_json

            elif None not in (jobReqId, jobProfile, channelName) and channelName == "Internal Posting" :

                response_text = "Posted Job " + jobReqId + " for " + str(jobProfile) + " on the " + str(channelName)
                response_json["response"] = response_text

                return response_json

            else :

                message = jsonify(Error='Invalid channel name')
                return make_response(message, 400)
        else : 

                message = jsonify(Error='Invalid inputs...')
                return make_response(message, 400)

            

        '''if None not in (jobReqId, jobProfile, channelName):
            response += jobReqId + " for " + str(jobProfile) + " on the " + str(channelName)
            response = {"response": response}
            print(response)
            return response
        else:
            return Response(
                {"Error": "The response body goes here"},
                status=400
            )'''



@app.route('/modifyDescComp', methods=['POST'])
def update_JDAndComp():
    if request.method == 'POST':
        input_josn = request.get_json()
        input_josn = input_josn['Job_Requisition']
        print(input_josn)
        input_josn['hiringManager'] = request.args.get("HiringManager")
        input_josn['recruiter'] = request.args.get("Recruiter")
        print("request.args.get(HiringManager) = " + request.args.get("HiringManager"))
        print("request.args.get(Recruiter) = " + request.args.get("Recruiter"))

        #Job_Requisition = input_josn['Job_Requisition']
        #Job_Requisition = mongo.db.WORecruitmentFlow.find_one( {"jobReqId": jobReqId},{"_id": 0} );
        # print(Job_Requisition)
        #Job_Requisition = request.get_json();
        # print(Job_Requisition)
        #Job_Requisition['jobReqLocale'][0]['jobDescription'] = job_description;
        mongo.db.WORecruitmentFlow.update_one(
            {"jobReqId": input_josn['jobReqId']}, {"$set": input_josn})
        Job_Requisition_JSON = {"Job_Requisition": input_josn}
        json_dumps = json.dumps(Job_Requisition_JSON, default=str)
        print("--------- Job_Requisition_JSON ---------")
        print(Job_Requisition_JSON)
        response = json.loads(json_dumps)
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
