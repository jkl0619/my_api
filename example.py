import os
import optparse
import requests
from requests.auth import HTTPBasicAuth

#THE EXAMPLE MUST BE INSTANTIATED WITH THE APPROPRIATE IP ADDRESS AND THE PORT OF THE SERVER
# -s ip -p port
# Parse through the arguments
parser = optparse.OptionParser()
parser.add_option('-s', dest='host', help='The host ip address to connect the client to')
parser.add_option('-p', dest='port', help='The port to connect to')
(options, args) = parser.parse_args()

# initialize values from command line
host = options.host
port = options.port

ownAddress = "http://" + host+ ":" +port

#THIS ONE ACCESSES THE FIRST POST METHOD AT ENDPOINT /status
address = ownAddress+"/status"
messagePayload = { 'message' : "hehe xd"}
r = requests.post(address, data=messagePayload, auth=HTTPBasicAuth('admin', 'pass'))
print(r.headers)
print(r.content)
print('\n')

#THIS ONE ACCESSES THE SECOND POST METHOD AT ENDPOINT /dm
address = ownAddress+"/dm"
messagePayload = { 'message' : "hehehXDDD", 'username' : 'jae06191'}
r = requests.post(address, data=messagePayload, auth=HTTPBasicAuth('admin', 'pass'))
print(r.headers)
print(r.content)
print('\n')

#THIS ONE ACCESSES THE FIRST GET METHOD AT ENDPOINT /firsttweetuser
address = ownAddress+"/firsttweetuser"
r = requests.get(address, auth=HTTPBasicAuth('admin', 'pass'))
print(r.headers)
print(r.content)
print('\n')

#THIS ONE ACCESSES THE SECOND GET METHOD AT ENDPOINT /firsttweetuser/friend
address = ownAddress+"/firsttweetuser/friend"
messagePayload = { 'username': 'jae06191'}
r = requests.get(address, data=messagePayload, auth=HTTPBasicAuth('admin', 'pass'))
print(r.headers)
print(r.content)
print('\n')


