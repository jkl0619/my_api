from zeroconf import ServiceBrowser, Zeroconf
import os
import time
from twitter import *
from flask import Flask, request, render_template, redirect, abort, flash, jsonify

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

zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()

#curl -H "Authorization: Bearer <ACCESS-TOKEN>" "https://canvas.instructure.com/api/v1/courses"

# curl "https://canvas.instructure.com/api/v1/courses?access_token=<ACCESS-TOKEN>"

#address = '\xc0\xa8\x01\x8f'
# they are hex values
#ipv4_address = ':'.join(str(ord(i)) for i in address)

# coding: utf-8

app = Flask(__name__)  # create our flask app

# configure Twitter API
twitter = Twitter(
    auth=OAuth(os.environ.get('OAUTH_TOKEN'), os.environ.get('OAUTH_SECRET'),
               os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))

)


@app.route('/')
def main():
    # fetch 3 tweets from my account
    myTweets = twitter.statuses.user_timeline(count=10)

    # fetch 3 tweets from ITP_NYU
    itpTweets = twitter.statuses.user_timeline(screen_name='itp_nyu', count=10)

    # app.logger.debug(itpTweets)

    templateData = {
        'title': 'My last three tweets',
        'myTweets': myTweets,
        'itpTweets': itpTweets
    }

    return render_template('index.html', **templateData)


@app.route('/search')
def search():
    # get search term from querystring 'q'
    query = request.args.get('q', '#redburns')

    # search with query term and return 10
    results = twitter.search.tweets(q=query, count=50)

    # return jsonify(results)
    # app.logger.debug(results)

    templateData = {
        'query': query,
        'tweets': results.get('statuses')
    }

    return render_template('search.html', **templateData)


@app.route('/post', methods=['GET', 'POST'])
def post_to_twitter():
    if request.method == 'POST':
        result = twitter.statuses.update(status=request.form.get('status'))

        app.logger.debug(result)

        # redirect to new twitter status post
        return redirect('http://www.twitter.com/%s/status/%s' % (result['user']['screen_name'], result.get('id')))

    else:
        return render_template('post_to_twitter.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# This is a jinja custom filter
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    pyDate = time.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')  # convert twitter date string into python date/time
    return time.strftime('%Y-%m-%d %H:%M:%S', pyDate)  # return the formatted date.


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
    app.debug = True

    port = int(os.environ.get('PORT', 5000))  # locally PORT 5000, Heroku will assign its own port
    app.run(host='0.0.0.0', port=port)