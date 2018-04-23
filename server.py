#have no idea if this actually goes into the server.py or not but everythings fine


from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/path/to/the/uploads/on/canvas"
canvasURL = 'https://canvas.vt.edu/groups/52695/files/'

@app.route("/canvas", methods = ['GET'])
def canvas():
	r = requets.get(canvasURL)
	json = r.json()
	files = json['filename']
	print(files)

@app.route("/canvas/download/<str:_filename>", methods = ['GET'])
def canvasDown(_filename):
	r = requests.get(canvasURL+'?'+filename, allow_redirects = True)
	open(filename, 'wb').write(r.content)
	return ''
	
	
@app.route("/canvas/upload/<str:_filename>/<str:_file>", methods = ['POST'])
def canvasUp(_filename, _file):
	f = request.files[_file]
	f.save(_filename)
	return ''
	
	
