# mongo_connection_string = """mongosh "mongodb+srv://cluster0.nldvj.mongodb.net/myFirstDatabase" --apiVersion 1 --username workbotadmin"""

def get_database(username, password, cluster_name, project_name, db_name):
    from pymongo import MongoClient

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://{username}:{password}@{cluster_name}.mongodb.net/{project_name}"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[db_name]
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    import random
    from urllib.parse import quote
    # Get the database
    username = "workbotadmin"
    password = quote("workbotpass@22_")
    cluster_name = "cluster0.nldvj"
    project_name = "rasa_faq"
    db_name="brain_teasers"

    client = get_database(
        username= username,
        password= password,
        cluster_name= cluster_name,
        project_name= project_name,
        db_name= db_name
    )
    print(password)
    collection = client['questions']
    RandomNumber = random.randint(0, collection.count_documents({})-1)

    result = collection.find({},{'_id':0}).limit(-1).skip(RandomNumber).next()
    try:
        q_id = result['q_id']
        question = result['question']
        options = list(result['options'].keys())
        print( {"q_id": q_id , "question": question, "options": options})
    except:
        print(False) 