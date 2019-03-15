#!/usr/bin/env python3

import sys
from omxplayer.player import OMXPlayer
from pathlib import Path
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

distSensado = 100
tgr = 1
slength = '1366'
swidth = '768'

print ("Distance measurement in progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

try:
    VIDEO_PATH = '/home/pi/Documents/biblioteca/sources/dummy/muertitos.mp4'
    player = OMXPlayer(VIDEO_PATH,  args=['--no-osd', '--loop', '--win', '0 0 {0} {1}'.format(slength, swidth)])
    time.sleep(1)

    print("Listo para usar")
    while True:
        player.pause()
        GPIO.output(TRIG, False)                 
        time.sleep(2)
                                

        GPIO.output(TRIG, True)                  
        time.sleep(0.00001)                      
        GPIO.output(TRIG, False)                 

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start 

        distance = pulse_duration * 17150        
        distance = round(distance, 2)    

        #Check whether the distance is within range
        if distance > 2 and distance < distSensado:
            #print ("Distancia:",distance - 0.5,"cm")
            print("Accion numero {}".format(tgr),"- Distancia:",distance - 0.5,"cm")
            player.play()
            time.sleep(player.duration())
            tgr = tgr + 1
        else:
            print ("Usuario fuera de rango")

        player.set_position(0.0)

except KeyboardInterrupt:
    player.quit()
    time.sleep(3)
    sys.exit()