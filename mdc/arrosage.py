#!/usr/bin/python3
#coding: utf-8
#Dernier update: 2018-11-18

#Ajout du transistor pour adapter 3.3V to 5V
import RPi.GPIO as GPIO
import time
import pickle
import datetime

sortie = 18
duree_arrosage = 14

#setup des sorties
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sortie,GPIO.OUT)
GPIO.setwarnings(False)

#variables globales
global event_arrosage

def ecriture_fichier():
    with open('/home/pi/mdc/event_arrosage','wb') as fichier:
        fichier_event_arrosage = pickle.Pickler(fichier)
        fichier_event_arrosage.dump(event_arrosage)

event_arrosage = {"etat_actuel":1}
ecriture_fichier()

GPIO.output(sortie,GPIO.HIGH)
etat = GPIO.input(sortie)
time.sleep(duree_arrosage)
GPIO.output(sortie,GPIO.LOW)

event_arrosage = {"etat_actuel":0}
event_arrosage["date_dernier_arrosage"] = datetime.date.today()
event_arrosage["heure_dernier_arrosage"] = datetime.datetime.now() \
                                           .strftime("%X")
event_arrosage["etat_arrosage"] = etat

ecriture_fichier()

GPIO.cleanup()
