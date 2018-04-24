import led_pins
import json
import sys
import time
import logging
from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo
import RPi.GPIO as GPIO
from flask import Flask, request, redirect, jsonify
import requests
import socket
import os

app = Flask(__name__)

GPIO.setmode(led_pins.led_pins['mode'])

#Setting each pin as an output and making it low 
GPIO.setup(led_pins.led_pins['red'], GPIO.OUT)
GPIO.setup(led_pins.led_pins['green'], GPIO.OUT)
GPIO.setup(led_pins.led_pins['blue'], GPIO.OUT)

	
r = GPIO.PWM(led_pins.led_pins['red'], 50)
g = GPIO.PWM(led_pins.led_pins['green'], 50) 
b = GPIO.PWM(led_pins.led_pins['blue'], 50)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))
ownAddress = s.getsockname()[0]

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    desc = {'path': '/~paulsm/'}

    info = ServiceInfo("_http._tcp.local.",
                       "led._http._tcp.local.",
                       socket.inet_aton(ownAddress), 5555, 0, 0,
                       desc, "ash-2.local.")

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

print("zeroconf register success!")



	
led_data ={
    'red':0.0,
    'green':0.0,
    'blue':0.0,
    'rate':0.0,
    'state':0
}

r.start(0)
g.start(0)
b.start(0)

@app.route("/led", methods = ['POST', 'GET'])
def led():
    if request.method == 'POST':

        dcr = 0.0
        dcg = 0.0
        dcb = 0.0
                
        redBool = 1
        greenBool = 1
        blueBool = 1
        
        try:
            if led_data['red'] > float(request.form['red']):
                redBool = 1
            led_data['red'] = float(request.form['red'])
        except:
            print("No new red value given. Previous one is still in use")
        try:
            if led_data['green'] > float(request.form['green']):
                greenBool = 1
            led_data['green'] = float(request.form['green'])
        except:
            print("No new green value given. Previous one is still in use")
        try:
            if led_data['blue'] > float(request.form['blue']):
                blueBool = 1
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
        print(str(redBool))
        print(str(greenBool))
        print(str(blueBool))
        try:
            if led_data['state'] == 1:
                if redBool == 1:
                    while dcr < led_data['red']+1:
                        r.ChangeDutyCycle(dcr)
                        print(str(dcr))
                        print(str(led_data['red']))
                        print("Redup")
                        dcr = dcr + 1.0;
                        time.sleep(led_data['rate'])
                else:
                    while dcr > -1:
                        print(str(redBool))
                        r.ChangeDutyCycle(dcr)
                        dcr = dcr - 1.0
                        print(str(dcr))
                        print("Reddown")
                        time.sleep(led_data['rate'])
                if greenBool == 1:    
                    while dcg < led_data['green']+1:
                        g.ChangeDutyCycle(dcg)
                        print(str(dcg))
                        dcg = dcg + 1.0;
                        time.sleep(led_data['rate'])
                else:
                    while dcg > -1:
                        g.ChangeDutyCycle(dcg)
                        dcg = dcg - 1.0
                        print(str(dcg))
                        time.sleep(led_data['rate'])
                if blueBool == 1:        
                    while dcb < led_data['blue']+1:
                        b.ChangeDutyCycle(dcb)
                        print(str(dcb))
                        dcb = dcb + 1.0;
                        time.sleep(led_data['rate'])
                else:   
                    while dcb > -1:
                        b.ChangeDutyCycle(dcb)
                        dcb = dcb - 1.0
                        print(str(dcb))
                        time.sleep(led_data['rate'])
        except KeyboardInterrupt:
            pass
        return "Data save successful" + "\n"
                        
    elif request.method == 'GET':
        retVal = json.dumps(led_data)
        return retVal + "\n"
    else:
        retVal = "Action could not be completed \n"
        return retVal

r.stop()
g.stop()
b.stop()
GPIO.cleanup()
	
	
if __name__ == "__main__":
	app.run(host=ownAddress, port = 5555, debug=True)		
	

