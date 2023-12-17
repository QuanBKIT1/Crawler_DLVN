from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from tqdm import tqdm 

uri = "mongodb+srv://ducquan:Quan16112002@cluster0.iliifpd.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
count_insert_doc = 0
duplicated_id = 0
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    database = client.get_database("data_science")
    database.get_collection("tour").drop()
    database.create_collection('tour')
    collection = database.get_collection("tour")
    
    with open("./DuLichVietTour_v3.json", "r", encoding='utf-8') as file:
        json_data = json.load(file)
    # collection.insert_many(json_data)

    for data in tqdm(json_data):
        existing_document = collection.find_one({"ticket_ID": data['ticket_ID']})
        if existing_document:
            duplicated_id += 1
        else:
            # Insert your new document here
            collection.insert_one(data)
            count_insert_doc += 1
    print("Duplicate ", duplicated_id, " documents")
    print("\nInsert to database ", count_insert_doc, " documents")

    client.close()
except Exception as e:
    print(e)
