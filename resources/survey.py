from flask import Flask, jsonify
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
from models.survey import Surveymodel
from models.user import UserModel
from pprint import pprint

class Survey(Resource):
    
    @jwt_required
    def post(self):
        data = request.get_json()
        
        #data = Survey.parser.parse_args()
        pprint('survey post method')
        surveyindb = Surveymodel.find_by_surveyname(data['survey_name'])
        if surveyindb:
            return {"message": "Survey with that Name already exists."}, 400
        
        

        survey_tobecreated = Surveymodel.requestmapper(data)
        
        survey = survey_tobecreated.save()
        
        if survey_tobecreated:
            pprint(survey_tobecreated._id)
            return {"message": "Survey created successfully.", "survey_id": survey_tobecreated._id}, 201
        else:
            return {"message": "Survey Not Created."}
    
    @jwt_required
    def put(self):
        data = request.get_json()
        
        pprint('survey Update method')
        surveyindb = Surveymodel.find_by_surveyname(data['survey_name'])
        if surveyindb is None:
            return {"message": "Survey with that Name doesn't exist."}, 400
        
        survey_tobeupdated= Surveymodel.requestmapper(data)
        survey_tobeupdated._id = data['survey_id']
        survey_updated = survey_tobeupdated.save()
        
        if survey_updated:
            pprint(survey_updated._id)
            return {"message": "Survey updated successfully.", "survey_id": survey_updated._id}, 201
        else:
            return {"message": "Survey Not Created."}

    @jwt_required
    def get(self):
        
        pprint("reached survey array method")
        client = pymongo.MongoClient("mongodb://balamuruganraja:Tcs2020@test1-shard-00-00-apxrb.azure.mongodb.net:27017,test1-shard-00-01-apxrb.azure.mongodb.net:27017,test1-shard-00-02-apxrb.azure.mongodb.net:27017/test?ssl=true&replicaSet=Test1-shard-0&authSource=admin&retryWrites=true&w=majority")
        userdb = client["User"]
        userlist = userdb["userlist"]
        usercursor = userlist.find()
        userarray = []
        for userobj in usercursor:
                userarray.append({ 'userid': userobj['_id'], 'email': userobj['email'], 'username': userobj['username'], 'password': userobj['password'] })
                pprint(userobj)
        pprint(userarray)
        return userarray


class Surveydata(Resource):
    #@jwt_required()
    def get(self,name):
        surveyindb = Surveymodel.find_by_surveyname(name)
        if surveyindb:
            return surveyindb
        else:
            return {"message": "No such Survey exists."}

class SurveyfromID(Resource):
    #@jwt_required()
    def get(self,survey_id):
        surveyindb = Surveymodel.find_by_surveyid(survey_id)
        if surveyindb:
            return surveyindb
        else:
            return {"message": "No such Survey exists."}

class SurveyArray(Resource):
    @jwt_required
    def get(self, creator_id):
        surveysindb = Surveymodel.find_all_surveys_for_userid(creator_id)
        if surveysindb:
            return surveysindb
        else:
            return {"message": "No Surveys found."}

class Surveyresponse(Resource):

    def post(self):
        pprint('surveyresponse post method')
        data = request.get_json()
        
        if data['participant_id'] != 1 and Surveymodel.get_sur_res_by_part_id(data['survey_id'], data['participant_id']):
            return {"message": "Survey response for this Participant already exists."}, 208
        else :
            surveres_tobecreated = Surveymodel.surveyresmapper(data)
            surveyres = surveres_tobecreated.save()
            if surveyres:
                pprint(surveyres._id)
                return {"message": "Survey Response Submitted successfully."}, 201
            else:
                return {"message": "Survey Response Not Submitted."}
        

class GetSurveyResponses(Resource):
    @jwt_required
    def get(self, survey_id):
        pprint('surveyresponse get method')
        
        survey_respones = Surveymodel.get_sur_res_by_surveyid(survey_id)
        if survey_respones:
            return survey_respones
        else:
            return {"message": "Survey Response not found"}

class SurveyCompare(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        
        pprint('survey compare post method')
        surveyindb = Surveymodel.find_by_surveyname(data['survey_name'])
        if surveyindb:
            return {"message": "Survey with that Name already exists."}, 400
        
        

        survey_tobecreated = Surveymodel.requestmapper(data)
        
        survey = survey_tobecreated.save()
        
        if survey_tobecreated:
            pprint(survey_tobecreated._id)
            return {"message": "Survey created successfully.", "survey_id": survey_tobecreated._id}, 201
        else:
            return {"message": "Survey Not Created."}
        
        

