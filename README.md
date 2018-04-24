"# my_api" 

MAKE SURE OUR ENDPOINTS ARE ALL LOWERCASE


****************************
  CONFIGURATIONS TO BE MADE
****************************

NEEDS TO HAVE THE FOLLOWING:

    pip3 install twitter on custom.py

    pip3 install flask_httpauth on server.py



****************************
         CUSTOM.PY
****************************

Custom.py uses the twitter api. In order to run this system, a special configuration would need to be made on the raspberry pi.

pip3 install twitter

The custom.py also utilizes the client_keys_twitter.py file in order to obtain the necessary access tokens of the user.

The custom.py can perform 2 different GET methods and 2 different POST methods

@app.route('/status', methods = ['POST'])
endpoint: /status
parameter: message
parameter type: string
method = post
Updates the status of the user with the specified message.
CANNOT HAVE DUPLICATE STATUS. WILL RETURN AN ERROR IF TRYING TO RETURN A DUPLICATE ERROR MESSAGE

@app.route('/dm', methods = ['POST'])
endpoint: /dm
parameter: username, message
parameter type: string, string
method = post
Sends a direct message from the default user specified with the token, to the specified user, with the contents being the message
Use %20 instead of space for the message argument.

@app.route('/firstTweetUser', methods=['GET'])
endpoint: /firstTweetUser
parameter: N/A
parameter type: N/A
method = GET
Returns the user of the first tweet on your timeline.

@app.route('/firstTweetUser/friend', methods=['GET'])
endpoint: /firstTweetUser/friend
parameter: username
parameter type: string
method = GET
Returns the user of the first tweet on the specified users timeline.
Both the token user and the specified user should be followers of each other.

For more information, please take a look at the custom.pdf for the specific documentation

****************************
       Workload Share
****************************

Chris Miller -

    server.py

    mongodb_setup.py

Hao Nguyen -

    led.py


Jae Lee - jae0619@vt.edu:

    client_keys_twitter.py

    custom.py

    example.py

    zeroconf

    part of server.py

    custom api documentation
