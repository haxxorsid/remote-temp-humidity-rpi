import requests 
import threading
import math  
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep

#declare global vars for settings, humidity, temperature, speed
lowh, lowt, mediumh, mediumt, highh, hight = (-1,)*6
humidity, temperature = -1, -1
speed = None

#manual/auto setting id
setting_id = -1

#setup GPIO for motor and software PWM
#refer https://www.instructables.com/id/DC-Motor-Control-With-Raspberry-Pi-and-L293D/
#and http://www.rhydolabz.com/wiki/?p=11288
#for pin configuration for Motor speed adjustment, software PWM
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
pwm=GPIO.PWM(22, 100)
pwm.start(0)

def settings_update():
    #utilize global vars
    global lowh, lowt, mediumh, mediumt, highh, hight, humidity, temperature
    global speed, setting_id

    #first fetch manual setting from server
    manual_setting_update_url = 'http://localhost/site/api/manual.php'
    manual_setting_update_data = {'type':'RECENT'} 
    r = requests.post(url = manual_setting_update_url, data = manual_setting_update_data) 
    try:
        #get json data
        data = r.json()
    except ValueError:
        #print error and exit program if data received is not json, r.json might be b'false'
        print('Unable to fetch manual-setting!')
        exit()

    #if manual-setting returns empty array
    if data == False:
        speed = None
    else :
        #set speed to speed received, save id
        speed = data['speed']
        setting_id = data['id']

    #if manual-setting is None or manual setting is not set, fetch and use auto-setting
    if speed is None:
        #fetch auto-setting from server
        auto_setting_update_url = 'http://localhost/site/api/auto.php'
        auto_setting_update_data = {'type':'RECENT'} 
        r = requests.post(url = auto_setting_update_url, data = auto_setting_update_data) 
        try:
            #get json data
            data = r.json()
        except ValueError:
            #print error and exit program if data received is not json, r.json might be b'false'
            print('Unable to fetch auto-setting!')
            exit()
        #save auto-setting in global vars
        lowh = int(data['lowh'])
        lowt = int(data['lowt'])
        mediumh = int(data['mediumh'])
        mediumt = int(data['mediumt'])
        highh = int(data['highh'])
        hight = int(data['hight'])
        setting_id = data['id']
        #print auto-setting
        print('Settings (Auto) LowH: %s, MediumH: %s, HighH: %s, LowT: %s, MediumT: %s, HighT: %s'%(lowh, mediumh, highh, lowt, mediumt, hight))
    else :
        #print if manual-setting
        print('Settings (Manual) Speed: %s'%speed)

def sense():
    #use global vars
    global humidity, temperature

    #11 means DHT11, 4 is GPIO4 for signal
    #refer http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/
    pin = 4

    #save sensed data in vars
    humidity, temperature = Adafruit_DHT.read_retry(11, pin)
    #print sensed humidity, temperature
    print('Humidity: %s, Temperature: %s' % (humidity, temperature))

#for auto-setting calculate fan speed
def calc_fan_speed():

    #use global vars
    global lowh, lowt, mediumh, mediumt, highh, hight, humidity, temperature

    try:
        #calculate fan speed (low/medium/high) using distance formula
        x1 = (100/(highh-lowh))*(humidity-lowh)
        y1 = (100/(hight-lowt))*(temperature-lowt)
        x2 = 0
        y2 = 0
        #a is distance between sensed (humidity, temperature) and (low humidity, low temperature)
        a = math.sqrt((x1-x2)**2+(y1-y2)**2)
        x2 = (100/(highh-lowh))*(mediumh-lowh)
        y2 = (100/(hight-lowt))*(mediumt-lowt)
        #b is distance between sensed (humidity, temperature) and (medium humidity, medium temperature)   
        b = math.sqrt((x1-x2)**2+(y1-y2)**2)
        x2 = 100
        y2 = 100
        #c is distance between sensed (humidity, temperature) and (high humidity, high temperature)   
        c = math.sqrt((x1-x2)**2+(y1-y2)**2)
    except ZeroDivisionError:
        print('High-low limit of temperature/humidity is same in settings causing ZeroDivisionError!')
        exit()

    #smallest of all three distances a,b,c.
    smallest = get_smallest(a,b,c)

    #if a is smallest, it means sensed (humidity, temperature) is much closer to (low humidity, low temperature) than medium/high
    #hence speed must be low.
    if smallest == a:
        return 'Low'
    elif smallest == b:
        return 'Medium'
    elif smallest == c:
        return 'High'
    else:
        print('Some unknown error occurred while calculating fan speed!')
        exit()
    
def get_smallest(a, b, c):
    if a < b:
        smallest = a
    else:
        smallest = b
    if c < smallest:
        smallest = c
    return smallest 

def set_fan_speed(speed):
    #use global var 
    global pwm
    #rotate in one direction
    GPIO.output(16, True)
    GPIO.output(18, False)
    GPIO.output(22, True)
    #if speed is low, then 0% speed (motor won't rotate)
    if speed == 'Low':
        pwm.ChangeDutyCycle(0)
    #if speed Medium, then speed is 25%
    elif speed == 'Medium':
        pwm.ChangeDutyCycle(25)
    #if speed High, then speed is 100%
    else:
        pwm.ChangeDutyCycle(100)
    #print speed
    print('Fan speed set: %s'%speed)

def send_humidity_temperature(setting_type):
    #send humidity, temperature
    send_data_url = "http://localhost/site/api/data.php"
    #setting_type ="auto_id" if setting is auto, else "manual_id" if manual
    send_data_data = {'type':'INSERT', 'humidity': humidity, 'temperature': temperature, setting_type: setting_id} 
    r = requests.post(url = send_data_url, data = send_data_data)
    if(r.content==b'true'):
        print('Data sent!')
    else:
        print('There was some error sending data!')
        exit()

def start():
    #use global var speed
    global speed
    #fetch setting auto/manual from server
    settings_update()
    #sense humidity, temperature using DHT11
    sense()
    #if speed none, calculate fan speed using distance formula from fetched auto-setting parameters
    if speed is None:
        set_fan_speed(calc_fan_speed())
        #send sensed humidity, temperature to server
        send_humidity_temperature("auto_id")
    #else use speed set manually to set motor speed
    else:
        set_fan_speed(speed)
        #send sensed humidity, temperature to server
        send_humidity_temperature("manual_id")
    #run start() function again after 5 seconds
    threading.Timer(5.0, start).start()

#bootstrap start() function
start()