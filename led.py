#import led_pins
import json
import time
#import RPi.GPIO as GPIO
from flask import Flask, request, redirect, jsonify
import requests
import os

app = Flask(__name__)

#RPi.GPIO.setmode(led_pins['mode'])

#Setting each pin as an output and making it low
#GPIO.setup(led_pins['red'], GPIO.OUT)
#GPIO.setup(led_pins['green'], GPIO.OUT)
#GPIO.setup(led_pins['blue'], GPIO.OUT)

	
#r = GPIO.PWM(led_pins['red'], 50)
#g = GPIO.PWM(led_pins['green'], 50) 
#b = GPIO.PWM(led_pins['blue'], 50)  


	
led_data ={
    'red':0.0,
    'green':0.0,
    'blue':0.0,
    'rate':0.0,
    'state':0
}
 
@app.route("/led", methods =['GET'])
def led_get():
	retVal = json.dumps(led_data)
	return retVal

@app.route("/led/<path:varargs>", methods = ['POST'])
def led(varargs=None):

    listarg = varargs.split("/")
    count = 0        
    if len(varargs)%2 == 1:
        for count in range(len(listarg)):
            if listarg[count] == 'red':
                led_data['red'] = float(listarg[count+1])
            if listarg[count] == 'green':
                led_data['green'] = float(listarg[count+1])
            if listarg[count] == 'blue':
                led_data['blue'] = float(listarg[count+1])
            if listarg[count] == 'rate':
                led_data['rate'] = float(listarg[count+1])
            if listarg[count] == 'state':
                led_data['state'] = int(listarg[count+1])
        successstr = "Success! New data values set \n"
    else:
        return "Failure to set new data values."
    
    return json.dumps(led_data) +"\n" + json.dumps(listarg) + "\n"
        #eturn successstr
#    else:
#        errorstr = "Error: Failed to set values. \n"
#        return errorstr
		
try:
    while led_data['state'] == 1:
        print("poop")
        for dcr in range(0, led_data['red']+1, 1):
            #r.ChangeDutyCycle(dc)
            print(str(dcr))
            time.sleep(rate)
                
        for dcr in range(led_data['red'], -1, -1):
        #           r.ChangeDutyCycle(dc)
            print(str(dcr))
            time.sleep(rate)

                
        for dcg in range(0, led_data['green']+1, 1):
        #            r.ChangeDutyCycle(dc)
            print(str(dcg))
            time.sleep(rate)
                
        for dcg in range(led_data['green'], -1, -1):
        #           r.ChangeDutyCycle(dc)
            print(str(dcg))
            time.sleep(rate)
                
        for dcb in range(0, led_data['blue']+1, 1):
        #            r.ChangeDutyCycle(dc)
            print(str(dcb))
            time.sleep(rate)
                
        for dcb in range(led_data['blue'], -1, -1):
        #           r.ChangeDutyCycle(dc)
            print(str(dcb))
            time.sleep(rate)
	
except KeyboardInterrupt:
	pass

#r.stop()
#g.stop()
#b.stop()
#GPIO.cleanup()
	
	
if __name__ == "__main__":
	app.run(host='127.0.0.1', port = 5555, debug=True)		
	

