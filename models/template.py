from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
from flask_restful import Resource, reqparse
from pprint import pprint
from flask_jwt import jwt_required
from data.template import Template
from data.tabstructure import Tabstructure
from data.tabquestion import TabQuestion
from pprint import pprint
import json
from models.user import UserModel
class Templatemodel(Resource):
    
    
    def find_by_templatename(templatename) -> Template:
        
        existingtemplateobject = Template.objects(name=templatename).first()
        if existingtemplateobject:
            templateobject = existingtemplateobject.to_json()
            return templateobject
        else:
            return existingtemplateobject
    
      
    def find_by_templateid(templateid) -> Template:
        
        templateobject = Template.objects(_id=templateid).first()
                
        if templateobject:
            pprint(templateobject.name)
        else:
            templateobject = None
        return templateobject

   
    
    def find_all_templates()  -> Template:
        template = Template()
        
        queryset = Template.objects().order_by('-_id')
        
        template_collection = []
        for template_obj in queryset:
            
            taglist = []
            for tag in template_obj['tags'] :
                taglist.append(tag)
            user = UserModel.finduser_by_user_id(template_obj.templatecreator_id)
            if user:
               t_creator_name = user['username']
            else:
                t_creator_name = "Anonymous"

            template_object = {'template_id': template_obj._id, 'template_name':template_obj.name, 'templatecreator_id': template_obj.templatecreator_id, 't_creator_name': t_creator_name, 'taglist' : taglist}
            template_collection.append(template_object)

        return template_collection
   
    
    def requestmapper(data)  -> Template:
        
        template = Template()
        template.name =data['template_name']

        temp_taglist = []
        for tag in data['tags']:
            temp_taglist.append(tag)
        
        template.tags = temp_taglist
        template.templatecreator_id = data['templatecreator_id']

        temp_tablist = []
        for tab in data['tabs']:
            tabobject = Tabstructure()
            tabobject.tabname = tab['tabname']
            tabquestionobjectlist = []
            for tabitem in tab['tabquestions']:
                tabquestionobject= TabQuestion()
                tabquestionobject.q_id = tabitem['q_id']
                tabquestionobject.q_text = tabitem['q_text']
                tabquestionobject.q_responsetype = tabitem['q_responsetype']
                if tabquestionobject.q_responsetype == "select" :
                    responseoptions =[]
                    for resoption in tabitem['q_responseoptions']:
                        responseoptions.append(resoption)
                    tabquestionobject.q_responseoptions= responseoptions
                tabquestionobjectlist.append(tabquestionobject)
            tabobject.tabquestions = tabquestionobjectlist
            temp_tablist.append(tabobject)

        template.tabs = temp_tablist            
        return template
    
    #Method not in use
    def responsemapper(queriedtemplate):
        responsetemplate = [{'template_id': queriedtemplate._id, 'template_name':queriedtemplate.name, "tags":[] }]
        tabquestions= []
        responsetemplate['_id': queriedtemplate._id]
        responsetemplatetags= []
        for tags in queriedtemplate.tags:
            responsetemplatetags.append(tags)
        
        responsetabs = []
        for tabs in queriedtemplate.tabs:
            tab_questions = []
            for question in queriedtemplate.tabs.tabquestions:
                response_options = []
                for response in queriedtemplate.tabs.tabquestions.responseoptions:
                    response_question = [{'q_id': question.q_id, 'q_text': question.q_text, 'responseoptions':[]} ]
            response_tab= [{'tabname': tabs.tabname, 'tab_questions': []}]
            responsetabs.append()
        responsearray = []
        template = Template()
        template.name =data['template_name']

        temp_taglist = []
        for tag in data['tags']:
            temp_taglist.append(tag)
        
        template.tags = temp_taglist

        temp_tablist = []
        for tab in data['tabs']:
            tabobject = Tabstructure()
            tabobject.tabname = tab['tabname']
            tabquestionobjectlist = []
            for tabitem in tab['tabquestions']:
                tabquestionobject= TabQuestion()
                tabquestionobject.q_id = tabitem['q_id']
                tabquestionobject.q_text = tabitem['q_text']
                responseoptions =[]
                for resoption in tabitem['q_responseoptions']:
                    responseoptions.append(resoption)
                tabquestionobject.q_responseoptions= responseoptions
                tabquestionobjectlist.append(tabquestionobject)
            tabobject.tabquestions = tabquestionobjectlist
            temp_tablist.append(tabobject)

        template.tabs = temp_tablist            
           
        return template
    
    
    def getcounter():
        template = Template()
        counter = 1
        firsttemplate = Template.objects().order_by('-_id').first()
        if firsttemplate:
            counter = (firsttemplate._id) + 1
            
        return counter
    

