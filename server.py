#have no idea if this actually goes into the server.py or not but everythings fine


from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/path/to/the/uploads/on/canvas"
#https://canvas.vt.edu/groups/52695/files is the file
canvasURL = 'https://canvas.vt.edu/api/v1/groups/52695/files'


@app.route("/canvas", methods = ['GET'])
def canvas():
	r = requests.get(canvasURL)
	json = r.json()
	files = json['filename']
	print(files)

@app.route("/canvas/<string:_filename>", methods = ['GET'])
def canvasDown(_filename):
	r = requests.get(canvasURL+'/'+_filename, allow_redirects = True)
	open(_filename, 'wb').write(r.content)
	return ''


@app.route("/canvas/<string:_filename>/<string:_file>", methods = ['POST'])
def canvasUp(_filename, _file):
	access_token = 'insert token here'
	api_url = canvasURL

	# Set up a session
	session = requests.Session()
	session.headers = {'Authorization': 'Bearer %s' % access_token}

	# Step 1 - tell Canvas you want to upload a file
	payload = {}
	payload['name'] = 'test.pdf'
	payload['parent_folder_path'] = '/'
	r = session.post(api_url, data=payload)
	r.raise_for_status()
	r = r.json()
	print(' ')
	print(r) # This successfully returns the expected response...

	# Step 2 - upload file
	payload = list(r['upload_params'].items())  # Note this is now a list of tuples
	print(' ')
	print(payload)
	with open('test.pdf', 'rb') as f:
		file_content = f.read()
	payload.append((u'file', file_content))  # Append file at the end of list of tuples
	r = requests.post(r['upload_url'], files=payload)
	r.raise_for_status()
	r = r.json()  # The requests now works and returns response 200 - not 301.
	print(' ')
	print(r)# This is a dictionary containing some info about the uploaded file


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)
