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


@app.route("/led", methods = ['POST', 'GET'])
def led():
    if request.method == 'POST':

        dcr = 0.0
        dcg = 0.0
        dcb = 0.0
        
        try:
            led_data['red'] = float(request.form['red'])
        except:
            print("No new red value given. Previous one is still in use")
        try:
            led_data['green'] = float(request.form['green'])
        except:
            print("No new green value given. Previous one is still in use")
        try:
            led_data['blue'] = float(request.form['blue'])
        except:
            print("No new blue value given. Previous one is still in use")
        try:
            led_data['rate'] = float(request.form['rate'])
        except:
            print("No new rate value given. Previous one is still in use")
        try:
            led_data['state'] = int(request.form['state'])
        except:
            print("No new state value given. Previous one is still in use")

        try:
            if led_data['state'] == 1:
                while dcr < led_data['red']+1:
                    #r.ChangeDutyCycle(dc)
                    print("Redup")
                    dcr = dcr + 1.0;
                    time.sleep(5)
                while dcr > -1:
                    dcr = dcr - 1.0
                    print("Reddown")
                    time.sleep(led_data['rate'])
                    
                while dcg < led_data['green']+1:
                    #r.ChangeDutyCycle(dc)
                    print(str(dcg))
                    dcg = dcg + 1.0;
                    time.sleep(led_data['rate'])
                while dcg > -1:
                    dcg = dcg - 1.0
                    print(str(dcg))
                    time.sleep(led_data['rate'])
                    
                while dcb < led_data['blue']+1:
                    #r.ChangeDutyCycle(dc)
                    print(str(dcb))
                    dcb = dcb + 1.0;
                    time.sleep(led_data['rate'])
                while dcb > -1:
                    dcb = dcb - 1.0
                    print(str(dcb))
                    time.sleep(led_data['rate'])
        except KeyboardInterrupt:
            pass
        return json.dumps(led_data) + "\n" + "Data save successful" + "\n"
                        
    elif request.method == 'GET':
        retVal = json.dumps(led_data)
        return retVal + "\n"
    else:
        retVal = "Action could not be completed \n"
        return retVal

#r.stop()
#g.stop()
#b.stop()
#GPIO.cleanup()
	
	
if __name__ == "__main__":
	app.run(host='127.0.0.1', port = 5555, debug=True)		
	

