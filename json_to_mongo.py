from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

uri = "mongodb+srv://ducquan:Quan16112002@cluster0.iliifpd.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    database = client.get_database("data_science")
    collection = database.get_collection("tour")
    
    with open("", "r") as file:
        json_data = json.load(file)
    collection.insert_many(json_data)
    client.close()
except Exception as e:
    print(e)
