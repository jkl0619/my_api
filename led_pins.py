"""
DO NOT change the key values in this dictionary.
DO NOT add additional key-value pairs to this dictionary.

Feel free to modify the values of the current keys to whatever pin values and mode is relevant for your specific LED setup.

Note: You do not need to do an if-else check for led_pins['mode'].
Internally, BOARD is represented by the integer 10 while BCM is represented by the integer 11.

Something like RPi.GPIO.setmode(led_pins['mode']) will work.

Example: 

led_pins = {
'red': 25,
'green': 24,
'blue': 23,
'mode': 11}

"""

led_pins = {
'red': 11,
'green': 13,
'blue': 15,
'mode': 10}
