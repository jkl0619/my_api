from flask import Flask, request, redirect
from flask_httpauth import HTTPBasicAuth
import json
import mongodb_setup
import canvas_token
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/path/to/the/uploads/on/canvas"
canvasURL = 'https://canvas.vt.edu/api/v1/groups/52695/files'
foldersURL = 'https://canvas.vt.edu/api/v1/groups/52695/folders'

@app.route("/canvas", methods = ['GET'])
def canvas():
        token = canvas_token.canvas_token

        session = requests.Session()
        session.headers = {'Authorization': 'Bearer %s' % token}

        r = session.get(canvasURL)
        r = r.json()
        filenameDict = {}
        for x in range (0,len(r)):
            filenameDict.update({r[x]["display_name"]:str(r[x]["id"])})
        print(json.dumps(filenameDict, indent=4))
        return ''



@app.route("/canvas/<string:_filename>", methods = ['GET'])
def canvasDown(_filename):
        token = canvas_token.canvas_token

        session = requests.Session()
        session.headers = {'Authorization': 'Bearer %s' % token}

        r = session.get(canvasURL)
        r = r.json()
        filenameDict = {}
        found = False
        for x in range (0,len(r)):
            filenameDict.update({r[x]["display_name"]:str(r[x]["id"])})
            #print(r[x]["display_name"] + " : " + str(r[x]["id"]))
        for x in range (0,len(r)):
            if r[x]["display_name"] == _filename:
                DL = session.get(r[x]["url"])
                open(_filename, 'wb').write(DL.content)
                found = True
        if found == False:
            print("file not located")
        return ''


@app.route("/canvas/<string:_filename>/<string:_file>", methods = ['POST'])
def canvasUp(_filename, _file):
        pwd = os.getcwd()
        filePath = pwd+"/"+_file
        fileInfo = {
                    "name":_filename,
                    "parent_folder_path": "/"
                    }
        
        token = canvas_token.canvas_token

        session = requests.Session()
        session.headers = {'Authorization': 'Bearer %s' % token}

        r = session.get(foldersURL)
        r = r.json()
        r = session.post(canvasURL, data = fileInfo)        
        r.raise_for_status()
        r = r.json()
        
        payload = list(r["upload_params"].items())
        with open(_file, 'rb') as file:
            fileContent = file.read()
        payload.append((u'file', fileContent))
        r = requests.post(r["upload_url"],files=payload)
        r.raise_for_status()
        r=r.json()
        return ''



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5555, debug=True)
