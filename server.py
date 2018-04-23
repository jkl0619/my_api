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
        canvasStatus = r.status_code
        if canvasStatus != 200:
            return "Failed. Status Code: " + str(canvasStatus) + '\n'
        r = r.json()
        filenameDict = {}
        for x in range (0,len(r)):
            filenameDict.update({r[x]["display_name"]:str(r[x]["id"])})
        return "Status Code: " + str(canvasStatus) + "\n" + json.dumps(filenameDict, indent=4)
        


@app.route("/canvas/download", methods = ['GET'])
def canvasDown():
        token = canvas_token.canvas_token

        session = requests.Session()
        session.headers = {'Authorization': 'Bearer %s' % token}

        _filename = request.args.get('filename', None)
        if _filename == None:
            return "URL parameter input is incorrect.\n"
        
        
        r = session.get(canvasURL)
        canvasStatus = r.status_code
        r = r.json()
        filenameDict = {}
        found = False
        for x in range (0,len(r)):
            filenameDict.update({r[x]["display_name"]:str(r[x]["id"])})
        for x in range (0,len(r)):
            if r[x]["display_name"] == _filename:
                DL = session.get(r[x]["url"])
                DLstatus = DL.status_code
                open(_filename, 'wb').write(DL.content)
                found = True
                
        if found == False and canvasStatus == 200:
            return "File does not exist in canvas folder.\n"
        return "Canvas connection: " + str(canvasStatus) + "   File download: " + str(DLstatus) + "\n"


@app.route("/canvas/upload", methods = ['POST'])
def canvasUp():
        _filename = request.form['filename']
        _file = request.files['file']
    
        fileInfo = {
                    "name":_filename,
                    "parent_folder_path": "/"
                    }
        
        token = canvas_token.canvas_token

        session = requests.Session()
        session.headers = {'Authorization': 'Bearer %s' % token}

        r = session.get(foldersURL)
        canvasStatus = r.status_code
        r = session.post(canvasURL, data = fileInfo)  
        r = r.json()
        
        payload = list(r["upload_params"].items())
        payload.append((u'file', _file))
        r = requests.post(r["upload_url"],files=payload)
        uploadStatus = r.status_code
        #r.raise_for_status()
        #=r.json()
        return " Canvas status code: " + str(canvasStatus) + "    Upload status code: " + str(uploadStatus) + "\n"



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5555, debug=True)
