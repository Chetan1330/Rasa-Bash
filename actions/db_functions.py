import pymongo, urllib, getpass
import random


def db_connection():
    client = pymongo.MongoClient("mongodb+srv://workbotadmin:workbotpass%4022_@cluster0.nldvj.mongodb.net/rasa_faq")
    return client


def show_brain_teaser():
    client = pymongo.MongoClient("mongodb+srv://workbotadmin:workbotpass%4022_@cluster0.nldvj.mongodb.net/rasa_faq")
    db = client['brain_teasers']
    collection = db['questions']
    RandomNumber = random.randint(0, collection.count_documents({})-1)

    result = collection.find({},{'_id':0}).limit(-1).skip(RandomNumber).next()
    try:
        q_id = result['q_id']
        question = result['question']
        options = list(result['options'].keys())
        return {"q_id": q_id , "question": question, "options": options}
    except:
        return False


def brain_teaser_answer_check(q_id, answer):
    client = pymongo.MongoClient("mongodb+srv://workbotadmin:workbotpass%4022_@cluster0.nldvj.mongodb.net/rasa_faq")
    db = client['brain_teasers']
    collection = db['questions']
    result = collection.find_one({'q_id': q_id}, {'_id':0})
    print(result)
    try:
        if result['options'][answer]:
            return True
        else:
            return False
    except:
        return False


def show_project_list(project_name):
    client = pymongo.MongoClient("mongodb+srv://workbotadmin:workbotpass%4022_@cluster0.nldvj.mongodb.net/rasa_faq")
    db = client['projects']
    collection = db['project_lists']
    result = collection.find_one({'project_name': project_name}, {'_id':0})
    if result:
        return result
    else:
        return False