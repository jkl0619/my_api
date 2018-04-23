import os
import socket
import optparse

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

ownAddress = host+ ":" +port

#THIS ONE ACCESSES THE FIRST POST METHOD AT ENDPOINT /status/<string:message>
address = ownAddress+"/status/wewlad%20We%20boutta%20Pass%20This%20Class -u admin:pass"
os.system("curl -X POST " + address)

#THIS ONE ACCESSES THE SECOND POST METHOD AT ENDPOINT /dm/<string:username>/<string:message>
address = ownAddress+"/dm/jae06191/hello%20buddy -u admin:pass"
os.system("curl -X POST " + address)

#THIS ONE ACCESSES THE FIRST GET METHOD AT ENDPOINT /firsttweetuser
address = ownAddress+"/firsttweetuser -u admin:pass"
os.system("curl -X GET " + address)

#THIS ONE ACCESSES THE SECOND GET METHOD AT ENDPOINT /firsttweetuser/friend/<string:username>
address = ownAddress+"/firsttweetuser/friend/jae06191 -u admin:pass"
os.system("curl -X GET " + address)

