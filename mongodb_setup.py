import pymongo



connection = pymongo.Connection()

db = connection["User_Info"]
accounts = db["accounts"]

accounts.insert({"username": "admin", 'password':'pass'})
accounts.insert({"username": "chris", 'password':'hello'})
accounts.insert({"username": "hao", 'password':'world'})
accounts.insert({"username": "jae", 'password':'gdi'})

#To look up the account
#cursor = db.accounts.find()
#accounts.find({"username":parameterHere})[0]

----------------------------------------------------------------------

from pymongo import MongoClient

client = MongoClient()

db = client["User_Info"]
accounts = db["accounts"]

accounts.insert({"username": "admin", 'password':'pass'})
accounts.insert({"username": "chris", 'password':'hello'})
accounts.insert({"username": "hao", 'password':'world'})
accounts.insert({"username": "jae", 'password':'gdi'})

#To look up the account
#cursor = db.accounts.find()
#accounts.find({"username":parameterHere})[0]


