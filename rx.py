import socket
import urllib2
import os
import RPi.GPIO as GPIO
import time

os.chdir("/var/www/epSLAVE")

# define output pins...
txPin = 18
rPin = 11
gPin = 15
bPin = 13

# set up GPIO...
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(txPin,GPIO.OUT)
GPIO.setup(rPin,GPIO.OUT)
GPIO.setup(gPin,GPIO.OUT)
GPIO.setup(bPin,GPIO.OUT)

rPWM = GPIO.PWM(rPin,50)
gPWM = GPIO.PWM(gPin,50)
bPWM = GPIO.PWM(bPin,50)

rPWM.start(0)
gPWM.start(100)
bPWM.start(100)

#//////////////////////////////////////////////
# READ SINGLE SETTING FUNCTION...
def readSetting(searchName):
        with open("settings.conf") as f:
                confString = f.readlines()
        try:
                for item in confString:
                        if not item[0] == '#':
                                item = item.strip("\n")
                                item = item.strip("\r")
                                item = item.split("=")
                                storedName = item[0]
                                storedValue = item[1]
                                if storedName == searchName:
                                        print "SETTING READ: " + searchName + " = " + storedValue
                                        return storedValue
        except:
                print "SETTING ERROR: NAME" + searchName + " NOT FOUND!"

#//////////////////////////////////////////////

#//////////////////////////////////////////////
# FUNCTION TO WRITE COLOR TO GPIO
def colorWrite(color):
        rgbLed = readSetting("RGBLED")
        if rgbLed == "ENABLED":
                brightness = int(readSetting("BRIGHTNESS"))
                if color == "kill":
                        rPWM.ChangeDutyCycle(100)
                        gPWM.ChangeDutyCycle(100)
                        bPWM.ChangeDutyCycle(100)
                # this writes colors to the LED
                elif color == "red":
                        rPWM.ChangeDutyCycle(100-brightness)
                        gPWM.ChangeDutyCycle(100)
                        bPWM.ChangeDutyCycle(100)
                elif color == "green":
                        rPWM.ChangeDutyCycle(100)
                        gPWM.ChangeDutyCycle(100-brightness)
                        bPWM.ChangeDutyCycle(100)
                elif color == "blue":
                        rPWM.ChangeDutyCycle(100)
                        gPWM.ChangeDutyCycle(100)
                        bPWM.ChangeDutyCycle(100-brightness)
#//////////////////////////////////////////////

def subscribeToHost(master,myIP,myFreq):
	url = 'http://'+master+'/addSlave.php?slaveIP='+myIP+'&slaveFreq='+myFreq
	response = urllib2.urlopen(url)
	print url
	print response.read()

def parseCommand(command):
	command = command.split(":")
	type = command[0]
	if type == "RF":
		com = "sudo nice -n -20 "+command[1]
		os.system(com)
	elif type == "RBT":
		os.system("sudo reboot")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
myIP = (s.getsockname()[0])
s.close()

print myIP
myFreq = readSetting("FREQ_ATTACHED")
master = readSetting("MASTER")

subscribeToHost(master,myIP,myFreq)

UDP_IP = str(myIP)
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1)

colorWrite("kill")
iteration = 0

while True:
	try:
		data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
		print "Received COM:", data
		data = str(data).split("\n")
		for item in data:
			if len(item) >= 3:
				colorWrite("green")
				parseCommand(item)
	except:
		colorWrite("blue")
		time.sleep(0.1)
		iteration += 1
		if iteration >= 60:
			iteration = 0
			subscribeToHost(master,myIP,myFreq)
		pass
	colorWrite("kill")
