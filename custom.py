from zeroconf import ServiceBrowser, Zeroconf
import os
from twitter import *
from flask import Flask, request, render_template, redirect, abort, flash, jsonify
from clientKeys import *

address = ""

class MyListener(object):
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        # print name, info.get_name(), info.server,
        print (name)
        print (info)
        address = info.server

print(address)

#zeroconf = Zeroconf()
#listener = MyListener()
#browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
#try:
#    input("Press enter to exit...\n\n")
#finally:
#    zeroconf.close()

#curl -H "Authorization: Bearer <ACCESS-TOKEN>" "https://canvas.instructure.com/api/v1/courses"

# curl "https://canvas.instructure.com/api/v1/courses?access_token=<ACCESS-TOKEN>"

#address = '\xc0\xa8\x01\x8f'
# they are hex values
#ipv4_address = ':'.join(str(ord(i)) for i in address)

# coding: utf-8

app = Flask(__name__)   # create our flask app

# configure Twitter API
twitter = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))


# configure Twitter API
# set consumer token + access token


#Use %20 for space in Curl, especially for messages
#updates the status with the specified message
@app.route('/status/<string:message>', methods = ['POST'])
def statusUpdate(message):
    twitter.statuses.update(status=message)
    updateMessage= "Updated the status saying: " + message
    return updateMessage

#Sends a message to the user specified
@app.route('/dm/<string:username>/<string:message>', methods = ['POST'])
def sendDM(username,message):
    twitter.direct_messages.new(
        user=username,
        text=message)
    updateMessage = "Sent the DM to " + username
    updateMessage = updateMessage + "with the message: " + message
    return updateMessage


@app.route('/firstTweetUser', methods=['GET'])
def first_Tweet():
    x = twitter.statuses.home_timeline()

    # The username of the first tweet on your timeline
    return x[0]['user']['screen_name']

@app.route('/firstTweetUser/friend/<string:username>', methods=['GET'])
def first_Tweet_Friend(username):
    x = twitter.statuses.user_timeline(screen_name=username)

    # The username of the first tweet on their timeline
    return x[0]['user']['screen_name']


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8090)