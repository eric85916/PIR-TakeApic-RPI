import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


camera = PiCamera()

user = "eric85916@gmail.com"                
pwd = "vydoilqhmmmhldpx"
to = "eric85916@gmail.com"

msg = MIMEMultipart()
msg["Subject"] = "Warning"
msg["From"] = user
msg["To"] = to

part = MIMEText("FXCK difficult project!")
msg.attach(part)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)                        #Read iutput from PIR motion sensor

seg = (4, 17, 27, 22, 23, 24, 25)

digits = {
    '0': (1, 1, 1, 0, 1, 1, 1),
    '1': (1, 0, 0, 0, 1, 0, 0),
    '2': (1, 1, 0, 1, 0, 1, 1),
    '3': (1, 1, 0, 1, 1, 1, 0),
    '4': (1, 0, 1, 1, 1, 0, 0),
    '5': (0, 1, 1, 1, 1, 1, 0),
    '6': (0, 1, 1, 1, 1, 1, 1),
    '7': (1, 1, 0, 0, 1, 0, 0),
    '8': (1, 1, 1, 1, 1, 1, 1),
    '9': (1, 1, 1, 1, 1, 1, 0)
}

for n in range(0, 7):
    GPIO.setup(seg[n], GPIO.OUT)
c = 0 
while True:
    i=GPIO.input(12)
    if i==0:                                      #When output from motion sensor is LOW
        time.sleep(.1)
    elif i==1:                                    #When output from motion sensor is HIGH
        c = 0
        for x in range(0, 4):                     #Countdown three seconds on 7seg
            for n in range(0, 7):
                GPIO.output(seg[n], digits[str(3 - c % 10)][n])
            time.sleep(1)
            c += 1
        
        camera.capture('/home/pi/Desktop/image.jpg')                 #Take a pic
        att1 = MIMEApplication(open("/home/pi/Desktop/image.jpg",'rb').read())
        att1.add_header('Content-Disposition','attachment',filename="test.jpg")
        msg.attach(att1)
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('eric85916@gmail.com','vydoilqhmmmhldpx')
        smtpObj.sendmail(user,to,msg.as_string())  #send an email
        smtpObj.close
        time.sleep(5)
