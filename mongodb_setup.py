from pymongo import MongoClient

client = MongoClient()

db = client["database"]
accounts = db["users"]

accounts.insert_one({"username": "admin", 'password':'pass'})
accounts.insert_one({"username": "chris", 'password':'hello'})
accounts.insert_one({"username": "hao", 'password':'world'})
accounts.insert_one({"username": "jae", 'password':'gdi'})

#To look up the account
#cursor = db.accounts.find()
#accounts.find({"username":parameterHere})[0]

