#!/usr/bin/python3
#coding: utf-8
#dernier update: 2018-11-18

#Ajout du transistor pour adapter 3.3V to 5V
import RPi.GPIO as GPIO
import time
from datetime import date
#from datetime import datetime
import datetime
import pickle
import os

duree_arrosage = 14

#setup de valeur initiale du moment d'arrosage
moment_dernier_arrosage = datetime.datetime.now() \
                          -datetime.timedelta(minutes=2)

while True:
    today = datetime.datetime.now()
    wd_now = date.weekday(today)
    hr_now = datetime.datetime.now().hour
    min_now = datetime.datetime.now().minute
    sec_now = datetime.datetime.now().second
    wn_now = date.today().isocalendar()
    
##    time.sleep(1)
##    print('wd',wd_now, 'time',hr_now,':',min_now)
##    print('Week number:',wn_now[1])
##    print('sec:',sec_now)
##    print(moment_dernier_arrosage)
    
##    #lecture du moment du dernier arrosage
##    with open('/home/pi/mdc/fichier_log','rb') as fichier:
##        fichier_log = pickle.Unpickler(fichier)
##        last_week = fichier_log.load()
##
    #lecture des moments d'arrosage programmés. données dans dictionnaire
    with open('/home/pi/mdc/moments_arrosage','rb') as fichier:
        fichier_moments_arrosage = pickle.Unpickler(fichier)
        moments_arrosage = fichier_moments_arrosage.load()

    if moments_arrosage[wd_now]==1 \
       and hr_now==moments_arrosage["hr"] \
       and min_now==moments_arrosage["min"] \
       and 0<=sec_now<duree_arrosage:
##       and today-moment_dernier_arrosage>datetime.timedelta(minutes=1):
       
        moment_dernier_arrosage = today
        #séquence d'arrosage
        os.system('python3 /home/pi/mdc/arrosage.py')

#GPIO.cleanup()

