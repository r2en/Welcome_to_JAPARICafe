#coding: utf-8
import RPi.GPIO as GPIO
from time import sleep
import commands

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN)

def main():
    while True:
        val = GPIO.input(25)
        print GPIO.input(25)
        if(val == True):
            welcome_to_japari_caffe()
        sleep(1)

def welcome_to_japari_caffe():
    #mp3 = commands.getoutput("mpg321 -q q02.mp3")
    mp4 = commands.getoutput("omxplayer -o local m.mp4")
    sleep(5)

if __name__ == '__main__':
    main()