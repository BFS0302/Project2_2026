import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage

channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

from_email_addr = "2328851784@qq.com"
from_email_pass = "pvyaxvobzgzjdibj"
to_email_addr = "2328851784@qq.com"

def send_email(status):
    msg = EmailMessage()
    if status == "dry":
       body = "Please water your plant"
       msg['Subject'] = "Plant Alert: Need Water"
    else:
       body = "Water NOT needed"
       msg['Subject'] = "Plant Status: OK"

    msg.set_content(body)
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr

    server = smtplib.SMTP('smtp.qq.com', 587)
    server.starttls()
    server.login(from_email_addr, from_email_pass)
    server.send_message(msg)
    server.quit()
    print("Email sent")

def check_moisture():
    if GPIO.input(channel):
        print("Water NOT Detected!")
        send_email("dry")
    else:
        print("Water Detected!")
        send_email("wet")
print("Monitoring started...")
try:
    while True:
        check_moisture()
        time.sleep(6 * 3600)
except KeyboardInterrupt:
    GPIO.cleanup()
