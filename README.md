# PIR-TakeApic-RPI
在家門口裝設人體紅外線感應模組偵測，偵測上門的陌生人，並驅動相機鏡頭自動拍攝，並以七節顯示器輔助倒數秒數，讓受攝者有時間喬好拍照姿勢，並將所拍攝的照片傳至我的信箱內加以查看。
# What do we need?
* Raspberry Pi 3
* PiCamera
* Seven-segment display
* PIR Motion Sensor
* Dupont Line*12
# PIR Motion Sensor
* 以下連結有詳細說明PIR Motion Sensor介紹
https://maker.pro/raspberry-pi/tutorial/how-to-interface-a-pir-motion-sensor-with-raspberry-pi-gpio
* PIR-TakeApic-RPI杜邦線接法請參照圖片  
![image](https://github.com/eric85916/PIR-TakeApic-RPI/blob/master/PIR1.jpg)
![image](https://github.com/eric85916/PIR-TakeApic-RPI/blob/master/PIR2.jpg)
# Seven-segment display
* 以下連結有詳細說明Seven-segment display介紹
* https://raspberrypi.readbook.tw/7seg.html
* PIR-TakeApic-RPI杜邦線接法請參照圖片
![image](https://github.com/eric85916/PIR-TakeApic-RPI/blob/master/7SEG1.jpg)
![image](https://github.com/eric85916/PIR-TakeApic-RPI/blob/master/7SEG2.jpg)
# Picamera
* 以下連結有詳細說明Picamera介紹
* https://projects.raspberrypi.org/en/projects/getting-started-with-picamera
* PIR-TakeApic-RPI的picamera裝法請參照圖片
![image](https://github.com/eric85916/PIR-TakeApic-RPI/blob/master/Picamera.jpg)
# Send & Receive the email
* 以下連結有詳細說明如何透過smtp來發送郵件
* https://ithelp.ithome.com.tw/articles/10196110
* https://blog.csdn.net/handsomekang/article/details/9811355
* 執行PIR-TakeApic-RPI後，所收到的信件如下
![image](https://github.com/eric85916/PIR-TakeApic-RPI/blob/master/ReceiveMail1.jpg)
![image](https://github.com/eric85916/PIR-TakeApic-RPI/blob/master/ReceiveMail2.jpg)
* 以下為執行PIR-TakeApic-RPI後所收到的照片
![image](https://github.com/eric85916/PIR-TakeApic-RPI/blob/master/ReceiveMail3.jpg)
* 以下為Demo影片
https://youtu.be/E2TAWfKsFVs
* 以下為PIR-TakeApic-RPI程式碼
# STEP1:#Read iutput from PIR motion sensor
# STEP2:Countdown three seconds on 7seg
# STEP3:Camera take a pic
# STEP4:Send&check the email&the photo 
```import RPi.GPIO as GPIO
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

seg = (4, 17, 27, 22, 23, 24, 25)              #Displaying the digits 0 to 9

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
        
        camera.capture('/home/pi/Desktop/image.jpg')                 #Camera take a pic
        att1 = MIMEApplication(open("/home/pi/Desktop/image.jpg",'rb').read())
        att1.add_header('Content-Disposition','attachment',filename="test.jpg")
        msg.attach(att1)
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('eric85916@gmail.com','vydoilqhmmmhldpx')
        smtpObj.sendmail(user,to,msg.as_string())  #send an email   #Send the email
        smtpObj.close
        time.sleep(5)
