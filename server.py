#have no idea if this actually goes into the server.py or not but everythings fine


from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/path/to/the/uploads/on/canvas"
canvasURL = 'https://www.canvas.com/'

@app.route("/canvas", methods = ['GET'])
def canvas():
	r = requets.get(canvasURL)
	json = r.json()
	files = json['filename']
	print(files)

@app.route("/canvas/<str:_filename>", methods = ['GET'])
def canvasDown(_filename):
	r = requests.get(canvasURL+'/'+filename, allow_redirects = True)
	open(filename, 'wb').write(r.content)
	return ''
	
	
@app.route("/canvas/<str:_filename>/<str:_file>", methods = ['POST'])
def canvasUp(_filename, _file):
	f = request.files[_file]
	f.save(_filename)
	return ''
	
	
@app.route("/canvas/<str:_filename1>/<str:_file1>/<str:_filename2>/<str:_file2>")	
def canvasUp2(_filename1. _filename2, _file1, _file2):
	f1 = request.files[_file1]
	f1.save(_filename1)
	f2 = request.files[_file2]
	f2.save(_filename2)
	return ''
	
