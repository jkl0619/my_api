import led_pins
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

@app.route("/poop", methods =['GET'])
def led_get():
	retVal = json.dumps(led_data)
	print(retVal)

# @app.route("/led/<path:varargs>", methods = ['POST'])
# def led(varargs = None):
	
	# varargs = varargs.split("/")
	
	# if varargs.length()%2 == 0:
		# for param in range(0, varargs.length(), 2):
			# print(str(param))
	# else:
		# print("Error: Failed to set values.")


@app.route("/led/red/<int:v1>", methods = ['POST'])
def led(v1):

	print(v1)



try:
	while led_data['state'] == 1:
		for dcr in range(0, led_data['red']+1, 1):
#            r.ChangeDutyCycle(dc)
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
	
