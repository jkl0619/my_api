from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo
import os
from twitter import *
from flask import Flask, request, render_template, redirect, abort, flash, jsonify
from clientKeys import *
from flask_httpauth import HTTPBasicAuth
import socket
import logging
import sys

ownAddress = socket.gethostbyname(socket.gethostname())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    desc = {'path': '/~paulsm/'}

    info = ServiceInfo("_http._tcp.local.",
                       "custom._http._tcp.local.",
                       socket.inet_aton(ownAddress), 8090, 0, 0,
                       desc, "ash-2.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)

print("zeroconf register success!")

class MyListener(object):
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        # print name, info.get_name(), info.server,
        print (name)
        print (info)
        print (info.server)


#zeroconf = Zeroconf()
#listener = MyListener()
#browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

#try:
#    input("Press enter to exit...\n\n")
#finally:
#    zeroconf.close()



# coding: utf-8

app = Flask(__name__)   # create our flask app
auth = HTTPBasicAuth()

# configure Twitter API
twitter = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

users = {
    "admin": "pass",
    "jae": "laroca69"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

#Use %20 for space in Curl, especially for messages
#updates the status with the specified message
@app.route('/status/<string:message>', methods = ['POST'])
@auth.login_required
def statusUpdate(message):
    twitter.statuses.update(status=message)
    updateMessage= "Updated the status saying: " + message
    return updateMessage

#Sends a message to the user specified
@app.route('/dm/<string:username>/<string:message>', methods = ['POST'])
@auth.login_required
def sendDM(username,message):
    twitter.direct_messages.new(
        user=username,
        text=message)
    updateMessage = "Sent the DM to " + username
    updateMessage = updateMessage + "with the message: " + message
    return updateMessage


@app.route('/firsttweetuser', methods=['GET'])
@auth.login_required
def first_Tweet():
    x = twitter.statuses.home_timeline()

    # The username of the first tweet on your timeline
    return x[0]['user']['screen_name']

@app.route('/firsttweetuser/friend/<string:username>', methods=['GET'])
@auth.login_required
def first_Tweet_Friend(username):
    x = twitter.statuses.user_timeline(screen_name=username)

    # The username of the first tweet on their timeline
    return x[0]['user']['screen_name']


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
    app.debug = True
    app.run(host=ownAddress, port=8090)