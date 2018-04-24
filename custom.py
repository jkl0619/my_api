from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo
import os
from twitter import *
from flask import Flask, request, render_template, redirect, abort, flash, jsonify
from client_keys_twitter import *
from flask_httpauth import HTTPBasicAuth
import socket
import logging
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
ownAddress = s.getsockname()[0]
#ownAddress = socket.gethostbyname(socket.gethostname())


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
    zeroconf.register_service(info)

print("zeroconf register success!")

app = Flask(__name__)   # create our flask app

# configure Twitter API
twitter = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

#Use %20 for space in Curl, especially for messages
#updates the status with the specified message
#@app.route('/status/<string:message>', methods = ['POST'])
@app.route('/status', methods = ['POST'])
def statusUpdate():
    f = request.form['message']
    twitter.statuses.update(status=f)
    updateMessage = "Updated the status saying: " + f
    return updateMessage + '\n'

#Sends a message to the user specified
@app.route('/dm', methods = ['POST'])
def sendDM():
    username = request.form['username']
    message = request.form['message']
    twitter.direct_messages.new(
        user=username,
        text=message)
    updateMessage = "Sent the DM to " + username
    updateMessage = updateMessage + " with the message: " + message
    return updateMessage + '\n'


@app.route('/firsttweetuser', methods=['GET'])
def first_Tweet():
    x = twitter.statuses.home_timeline()

    # The username of the first tweet on your timeline
    return x[0]['user']['screen_name'] + '\n'

@app.route('/firsttweetuser/friend', methods=['GET'])
def first_Tweet_Friend():
    username = request.args.get('username')
    x = twitter.statuses.user_timeline(screen_name=username)

    # The username of the first tweet on their timeline
    return x[0]['user']['screen_name'] + '\n'


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
    app.debug = True
    app.run(host=ownAddress, port=8090)
