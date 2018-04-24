from flask import Flask, request, redirect
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
import json
import canvas_token
import requests
import os
import logging
import socket
import sys

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                               #get IP address of the host
s.connect(('8.8.8.8' ,1))
ownAddress = s.getsockname()[0]

def on_service_state_change(zeroconf, service_type, name, state_change):                           #Found in source file given
    print("Service %s of type %s state changed: %s" % (name, service_type, state_change))
    global customname
    global ledname
    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            print("  Address: %s:%d" % (socket.inet_ntoa(info.address), info.port))
            print("  Weight: %d, priority: %d" % (info.weight, info.priority))
            print("  Server: %s" % (info.server,))
            if info.properties:
                print("  Properties are:")
                for key, value in info.properties.items():
                    print("    %s: %s" % (key, value))
            else:
                print("  No properties")
        else:
            print("  No info")
        print('\n')
    if(name == "custom._http._tcp.local."):
        customname = socket.inet_ntoa(info.address)
        customname = customname + ":"
        customname = customname+ str(info.port)
        #print(customname)
        
    if(name == "led._http._tcp.local."):
        ledname = socket.inet_ntoa(info.address)
        ledname = ledname + ":"
        ledname = ledname+ str(info.port)
        #print(ledname)



if __name__ == '__main__':                                                                             #found in source file given
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()
    print("\nBrowsing services, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])



app = Flask(__name__)                                                    #start flask server
canvasURL = 'https://canvas.vt.edu/api/v1/groups/52695/files'            
foldersURL = 'https://canvas.vt.edu/api/v1/groups/52695/folders'

auth = HTTPBasicAuth()                          #used to do the http authenication

client = MongoClient()                        #getting the mongo database
db = client["database"]
accounts = db["users"]

accountInfo = list(accounts.find())              #convert into list

accounts = {}

for x in range(0, len(accountInfo)):
        accounts[accountInfo[x]["username"]] = accountInfo[x]["password"]        #the get_pw was confusing if i kept it as the list above, so i changed it

@auth.get_password                                      #check for username in the database
def get_pw(username):
        if username in accounts:
            return accounts.get(username)
        return None
                                                                ###LED API###
@app.route("/led", methods = ['GET', 'POST'])             #get and post requests for the led Pi
@auth.login_required                                      #must be authenticated to request this
def led():
    if request.method == 'GET':                                  #this is used to pass the request along to the flask server
        ledURL = "http://" + ledname + "/led"                        #running on the led pi
        r = requests.get( ledURL )
        return r.content
    if request.method == 'POST':
        ledURL = "http://" + ledname + "/led"
        messagePayload = request.form
        r = requests.post( ledURL, messagePayload )
        return r.content
        
                                                                ###CUSTOM API###
@app.route("/status", methods = ['POST'])                       #functions below used to send data to the custom pi's flask server
@auth.login_required
def statusUpdate():
        customURL = "http://" + customname + "/status"
        messagePayload = { "message" : request.form["message"] }
        r = requests.post( customURL, data = messagePayload)
        return r.content
    

@app.route("/dm", methods = ['POST'])
@auth.login_required
def sendDM():
        customURL = "http://" + customname + "/dm"
        messagePayload = { "username" : request.form["username"],
                           "message" : request.form["message"]}
        r = requests.post( customURL, data = messagePayload)
        return r.content
    
@app.route("/firsttweetuser", methods = ['GET'])
@auth.login_required
def getFirstUser():
        customURL = "http://" + customname + "/firsttweetuser"
        r = requests.get(customURL)
        return r.content

@app.route("/firsttweetuser/friend", methods = ['GET'])
@auth.login_required
def getFirstFriend():
        messagePayload = { "username" : request.form["username"] }
        customURL = "http://" + customname + "/firsttweetuser"
        r = requests.get(customURL, data = messagePayload)
        return r.content


                                                            ###CANVAS API####
@app.route("/canvas", methods = ['GET'])
@auth.login_required
def canvas():
        token = canvas_token.canvas_token         #get the token from the canvas_token file

        session = requests.Session()              #start a session that will save the authority to open the canvas url based on the next sent header
        session.headers = {'Authorization': 'Bearer %s' % token}        #header that tells canvas that it can access it, since it has the token

        r = session.get(canvasURL)                 #this gets a list of the files found at this canvas url
        canvasStatus = r.status_code               #show the user the connection status code
        if canvasStatus != 200:      #200 means it went through fine
            return "Failed. Status Code: " + str(canvasStatus) + '\n'
        r = r.json()                   #convert file list into json object
        filenameDict = {}              
        for x in range (0,len(r)):        
            filenameDict.update({r[x]["display_name"]:str(r[x]["id"])})
        return "Status Code: " + str(canvasStatus) + "\n" + json.dumps(filenameDict, indent=4)          #display the status code and the list of the files
        


@app.route("/canvas/download", methods = ['GET'])
@auth.login_required
def canvasDown():
        token = canvas_token.canvas_token

        session = requests.Session()
        session.headers = {'Authorization': 'Bearer %s' % token}

        _filename = request.args.get('filename', None)              #get the file name that the client asks to download
        if _filename == None:
            return "URL parameter input is incorrect.\n"           #if the filename form was not found, there was an issue
        
        
        r = session.get(canvasURL)
        canvasStatus = r.status_code
        r = r.json()
        filenameDict = {}
        found = False
        for x in range (0,len(r)):
            filenameDict.update({r[x]["display_name"]:str(r[x]["id"])})
        for x in range (0,len(r)):
            if r[x]["display_name"] == _filename:                #if the filename was found in the files list
                DL = session.get(r[x]["url"])                        #get the URL accompanied with the file
                DLstatus = DL.status_code                            #get the status code for the cflient
                open(_filename, 'wb').write(DL.content)              #save the file from the given url and download it to the pwd
                found = True                    #this will demonstrate that the file was found
                
        if found == False and canvasStatus == 200:          #if canvas was successfully reached and the file just wasnt found
            return "File does not exist in canvas folder.\n"
        return "Canvas connection: " + str(canvasStatus) + "   File download: " + str(DLstatus) + "\n"


@app.route("/canvas/upload", methods = ['POST'])
@auth.login_required
def canvasUp():
        _filename = request.form['filename']            #_filename is the string holding the name that the client wants the file saved as
        _file = request.files['file']                    #the actual file found on the clients pwd
    
        fileInfo = {
                    "name":_filename,                   #canvas wants file info, presumably to decide where in the AWS to allot space
                    "parent_folder_path": "/"
                    }
        
        token = canvas_token.canvas_token

        session = requests.Session()
        session.headers = {'Authorization': 'Bearer %s' % token}

        r = session.get(foldersURL)
        canvasStatus = r.status_code
        r = session.post(canvasURL, data = fileInfo)                 #this will return back to the flask server what url to send the upload to
        r = r.json()
        
        payload = list(r["upload_params"].items())                   #this appends the payload to the upload paramters that canvas specifies
        payload.append((u'file', _file))
        r = requests.post(r["upload_url"],files=payload)              #send the file to the given url
        uploadStatus = r.status_code                                 #find the status code associated with the file upload
        return " Canvas status code: " + str(canvasStatus) + "    Upload status code: " + str(uploadStatus) + "\n"



if __name__ == "__main__":
    app.run(host=ownAddress, port=5555, debug=True)
