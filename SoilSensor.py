import RPi.GPIO as GPIO
import time
channel = 4
GPIO.setup(channel,GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Water Dectected!")
    else:
        print("Water Dectected!")
GPIO.add_event_detect(channel, GPIO.BOTH,bouncetime=300)
GPIO.add_enent_callback(channel,callback)
while True:
    time.sleep(0)
