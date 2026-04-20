import time
import smtplib
from email.message import EmailMessage
import RPi.GPIO as GPIO

FROM_EMAIL = "2328851784@qq.com"
EMAIL_PASS = "pvyaxvobzgzjdibj"
TO_EMAIL = "2328851784@qq.com"

SEND_TIMES = [(9, 0), (12, 0), (15, 0), (20, 0)]
SENSOR_PIN = 17
DRY_LEVEL = GPIO.LOW
CHECK_INTERVAL = 60
EMERGENCY_COOLDOWN = 3600

sent_index = set()
last_emergency_time = 0

def send_email(subject, content):
    try:
        msg = EmailMessage()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.set_content(content)
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(FROM_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        print("Email sent:", subject)
    except Exception as e:
        print("Failed:", e)

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN, GPIO.IN)

if __name__ == "__main__":
    init_gpio()
    start_date = time.localtime()
    start_date = (start_date.tm_year, start_date.tm_mon, start_date.tm_mday)

    try:
        while True:
            now = time.localtime()
            current_date = (now.tm_year, now.tm_mon, now.tm_mday)
            h, m = now.tm_hour, now.tm_min

            if current_date == start_date:
                for idx, (sh, sm) in enumerate(SEND_TIMES):
                    if idx not in sent_index and h == sh and sm <= m < sm + 1:
                        soil = "DRY" if GPIO.input(SENSOR_PIN) == DRY_LEVEL else "WET"
                        send_email(
                            f"Plant Status Update {idx+1}",
                            f"Check {idx+1}\nSoil: {soil}"
                        )
                        sent_index.add(idx)

            soil_val = GPIO.input(SENSOR_PIN)
            now_ts = time.time()
            if soil_val == DRY_LEVEL and now_ts - last_emergency_time >= EMERGENCY_COOLDOWN:
               send_email(
                   "URGENT: Soil Is Dry",
                   "Please water your plant immediately."
               )
               last_emergency_time = now_ts

            print(f"Time {h:02d}:{m:02d} | Sent today: {len(sent_index)}/4")
            time.sleep(CHECK_INTERVAL)

  except KeyboardInterrupt:
      print("\nStopped")
  finally:
      GPIO.cleanup()
