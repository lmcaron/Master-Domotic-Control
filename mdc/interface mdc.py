#!/usr/bin/python3
#Interface du Master Domotic Control
#Dernier update: 2018-11-18

import RPi.GPIO as GPIO
import tkinter
from tkinter import *
import math
import os
import time
from datetime import datetime
import subprocess
import pickle

#variables globales
global moments_arrosage
global event_arrosage
global duree_arrosage
moments_arrosage = {}
event_arrosage = {}
duree_arrosage = 14000   #en msec

#fonction d'arret du programme
def arret():
    root.destroy()
    os.system('pkill -f gestionnaire_domotique.py')
    GPIO.cleanup()
    print('opération arretée')

def ecriture_fichier():
    with open('/home/pi/mdc/moments_arrosage','wb') as fichier:
        fichier_moments_arrosage = pickle.Pickler(fichier)
        fichier_moments_arrosage.dump(moments_arrosage)
    print(moments_arrosage["hr"])
    print(moments_arrosage["min"])

def lecture_event():
    with open('/home/pi/mdc/event_arrosage','rb') as fichier:
            fichier_event_arrosage = pickle.Unpickler(fichier)
            event_arrosage = fichier_event_arrosage.load()

def update_subprocess():
    os.system('pkill -f gestionnaire_domotique.py')
    #run un script en parallele
    proc = subprocess.Popen("/home/pi/mdc/gestionnaire_domotique.py", shell=True, \
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("subrocess reparti")
    
class App:
    
    def __init__(self, master): #double underscore
        #Paramètre self permet de contenir toutes les variables (attributs, méthodes) propres à la classe
        frame1 = tkinter.Frame(master)#objet frame encapsulé dans l'objet root de classe App
        frame1.pack(fill=tkinter.BOTH, expand=1)#la couleur va remoplir toute la fenetre lorsque redimensionné
        frame1.configure(background='gray25')
        #height 1: une ligne de cette font entre dans le label        
        #tkinter.Label(frame1, text='Master Domotic Control',bg='gray25',fg='white',font='Time 35',height=1).grid(row=0,column=0)
        tkinter.Label(frame1, text='Master Domotic Control',bg='gray25',fg='white', \
                      font='Time 35',height=1).pack() 

        #definition des variables image des boutons
        self.icone_arrosage = PhotoImage(file='/home/pi/mdc/icone_arrosage4.png').subsample(2,2)
        self.icone_stop_arrosage = PhotoImage(file='/home/pi/mdc/icone_stop_arrosage.png') \
                                   .subsample(2,2)
        self.icone_dimanche = PhotoImage(file='/home/pi/mdc/btn_dimanche.png').subsample(3,3)
        self.icone_dimanche_checked = PhotoImage(file='/home/pi/mdc/btn_dimanche_checked.png') \
                                   .subsample(3,3)
        self.icone_lundi = PhotoImage(file='/home/pi/mdc/btn_lundi.png')
        self.icone_lundi = self.icone_lundi.subsample(3,3)
        self.icone_lundi_checked = PhotoImage(file='/home/pi/mdc/btn_lundi_checked.png')
        self.icone_lundi_checked = self.icone_lundi_checked.subsample(3,3)
        self.icone_mardi = PhotoImage(file='/home/pi/mdc/btn_mardi.png').subsample(3,3)
        self.icone_mardi_checked = PhotoImage(file='/home/pi/mdc/btn_mardi_checked.png') \
                                   .subsample(3,3)
        self.icone_mercredi = PhotoImage(file='/home/pi/mdc/btn_mercredi.png').subsample(3,3)
        self.icone_mercredi_checked = PhotoImage(file='/home/pi/mdc/btn_mercredi_checked.png') \
                                   .subsample(3,3)
        self.icone_jeudi = PhotoImage(file='/home/pi/mdc/btn_jeudi.png').subsample(3,3)
        self.icone_jeudi_checked = PhotoImage(file='/home/pi/mdc/btn_jeudi_checked.png') \
                                   .subsample(3,3)
        self.icone_vendredi = PhotoImage(file='/home/pi/mdc/btn_vendredi.png').subsample(3,3)
        self.icone_vendredi_checked = PhotoImage(file='/home/pi/mdc/btn_vendredi_checked.png') \
                                   .subsample(3,3)
        self.icone_samedi = PhotoImage(file='/home/pi/mdc/btn_samedi.png').subsample(3,3)
        self.icone_samedi_checked = PhotoImage(file='/home/pi/mdc/btn_samedi_checked.png') \
                                   .subsample(3,3)
        self.icone_arrosage_on = PhotoImage(file='/home/pi/mdc/icone_arrosage_on.png').subsample(5,5)
        self.icone_arrosage_off = PhotoImage(file='/home/pi/mdc/icone_arrosage_off.png') \
                                  .subsample(5,5)
        self.icone_update = PhotoImage(file='/home/pi/mdc/btn_update.png').subsample(3,3)


        #definition du frame d'arrosage
        frame2 = tkinter.LabelFrame(frame1, text='Arrosage', borderwidth=4,
                                    bg='gray25', fg='white', font='Time 15',
                                    padx=20, pady=20)
        frame2.pack(fill='both')

        #update l'app quand le pointeur passe dessus
        root.bind("<Enter>",self.update)

        #definition du bouton d'arrosage manuel
        self.button1 = tkinter.Button(frame2,bd=3,activebackground='white',command=self.arrosage) 
        self.button1.grid(row=1,column=0, sticky='w')
        self.button1.configure(image=self.icone_arrosage, compound='center')

        #definition des titres
        label1 = tkinter.Label(frame2, text='Arrosage manuel des plantes',
                               bg='gray25', fg='white',font='Time 18',height=1)
        label1.grid(row=0,column=0,columnspan=3, pady=10, sticky='w')
        
        label2 = tkinter.Label(frame2, text='Programmation des arrosages automatiques',
                               bg='gray25', fg='white',font='Time 18',height=1)
        label2.grid(row=2,column=0,columnspan=4, pady=10, sticky='w')

        label3 = tkinter.Label(frame2, text="Jours", bg='gray25', \
                                fg='white',font='Time 14',height=1)
        label3.grid(row=3,column=0,pady=5,sticky='w')
        
        label4 = tkinter.Label(frame2, text="Heure", bg='gray25', \
                                fg='white',font='Time 14',height=1)
        label4.grid(row=3,column=1,pady=5,sticky='w')

        label5 = tkinter.Label(frame2, text="Minute", bg='gray25', \
                                fg='white',font='Time 14',height=1)
        label5.grid(row=3,column=3,pady=5,sticky='w')
        
        label6 = tkinter.Label(frame2, text="Dernier arrosage", bg='gray25', \
                                fg='white',font='Time 14',height=1)
        label6.grid(row=8,column=1,columnspan=2, sticky='w')

        self.dernier_arrosage = StringVar()
        self.dernier_arrosage.set("")
        label7 = tkinter.Label(frame2, textvariable=self.dernier_arrosage, bg='gray25', \
                                fg='white',font='Time 30',height=1)
        label7.grid(row=9,column=1,columnspan=3, sticky='w')
        
        self.dernier_arrosage_hr = StringVar()
        self.dernier_arrosage_hr.set("")
        label8 = tkinter.Label(frame2, textvariable=self.dernier_arrosage_hr, bg='gray25', \
                                fg='white',font='Time 30',height=1)
        label8.grid(row=10,column=1,columnspan=3, sticky='w')

        self.dernier_arrosage_etat = IntVar()
        self.dernier_arrosage_etat.set("")
        label9 = tkinter.Label(frame2, textvariable=self.dernier_arrosage_etat, bg='gray25', \
                                fg='white',font='Time 12',height=1)
        label9.grid(row=10,column=4,sticky='w')

        label10 = tkinter.Label(frame2, text="etat:",bg='gray25',fg='white',font='Time 12')
        label10.grid(row=10,column=3,sticky="e")

        #boutons de sélections de semaines
        self.check_dimanche = tkinter.IntVar()
        self.check_lundi = tkinter.IntVar()
        self.check_mardi = tkinter.IntVar()
        self.check_mercredi = tkinter.IntVar()
        self.check_jeudi = tkinter.IntVar()
        self.check_vendredi = tkinter.IntVar()
        self.check_samedi = tkinter.IntVar()
        self.hr_arrosage = tkinter.IntVar()

        self.check_button_dimanche = tkinter.Checkbutton(frame2,variable=self.check_dimanche, \
                                                 bg='gray25',font='Time 15',\
                                                 indicatoron=0, \
                                                 selectimage=self.icone_dimanche_checked, \
                                                 command=self.update_jour)
        self.check_button_dimanche.configure(image=self.icone_dimanche, compound='center')
        self.check_button_dimanche.grid(row=4,column=0,pady=5,sticky='w')
        
        self.check_button_lundi = tkinter.Checkbutton(frame2,variable=self.check_lundi, \
                                                 bg='gray25',font='Time 15',\
                                                 indicatoron=0, \
                                                 selectimage=self.icone_lundi_checked, \
                                                 command=self.update_jour)
        self.check_button_lundi.configure(image=self.icone_lundi, compound='center')
        self.check_button_lundi.grid(row=5,column=0,pady=5,sticky='w')

        self.check_button_mardi = tkinter.Checkbutton(frame2,variable=self.check_mardi, \
                                                 bg='gray25',font='Time 15',\
                                                 indicatoron=0, \
                                                 selectimage=self.icone_mardi_checked, \
                                                 command=self.update_jour)
        self.check_button_mardi.configure(image=self.icone_mardi, compound='center')
        self.check_button_mardi.grid(row=6,column=0,pady=5,sticky='w')

        self.check_button_mercredi = tkinter.Checkbutton(frame2,variable=self.check_mercredi, \
                                                 bg='gray25',font='Time 15',\
                                                 indicatoron=0, \
                                                 selectimage=self.icone_mercredi_checked, \
                                                 command=self.update_jour)
        self.check_button_mercredi.configure(image=self.icone_mercredi, compound='center')
        self.check_button_mercredi.grid(row=7,column=0,pady=5,sticky='w')

        self.check_button_jeudi = tkinter.Checkbutton(frame2,variable=self.check_jeudi, \
                                                 bg='gray25',font='Time 15',\
                                                 indicatoron=0, \
                                                 selectimage=self.icone_jeudi_checked, \
                                                 command=self.update_jour)
        self.check_button_jeudi.configure(image=self.icone_jeudi, compound='center')
        self.check_button_jeudi.grid(row=8,column=0,pady=5,sticky='w')

        self.check_button_vendredi = tkinter.Checkbutton(frame2,variable=self.check_vendredi, \
                                                 bg='gray25',font='Time 15',\
                                                 indicatoron=0, \
                                                 selectimage=self.icone_vendredi_checked, \
                                                 command=self.update_jour)
        self.check_button_vendredi.configure(image=self.icone_vendredi, compound='center')
        self.check_button_vendredi.grid(row=9,column=0,pady=5,sticky='w')

        self.check_button_samedi = tkinter.Checkbutton(frame2,variable=self.check_samedi, \
                                                 bg='gray25',font='Time 15',\
                                                 indicatoron=0, \
                                                 selectimage=self.icone_samedi_checked, \
                                                 command=self.update_jour)
        self.check_button_samedi.configure(image=self.icone_samedi, compound='center')
        self.check_button_samedi.grid(row=10,column=0,pady=5,sticky='w')

        #liste des heures
        scrollbar = tkinter.Scrollbar(frame2, orient=VERTICAL)
        self.liste = tkinter.Listbox(frame2,bg='gray25', fg='white',font='Time 30', \
                                     selectbackground='green',selectforeground='white', \
                                     exportselection=0,yscrollcommand=scrollbar.set, \
                                     height=5,width=1,takefocus=1)
        for i in range(0,24):
            if 0<=i<10:
                self.liste.insert(i,"0"+str(i)+" :")
            else:
                self.liste.insert(i,str(i)+" :")                        
        
        self.liste.grid(row=4,column=1,rowspan=5,pady=5,sticky='new')
        scrollbar.configure(command=self.liste.yview)
        scrollbar.grid(row=4,column=2,rowspan=3,pady=5,sticky='nw')
##        self.liste.select_set(moments_arrosage["hr"])
        self.liste.bind('<<ListboxSelect>>',self.update_heure)

        #liste des minutes
        scrollbar2 = tkinter.Scrollbar(frame2, orient=VERTICAL)
        self.liste2 = tkinter.Listbox(frame2,bg='gray25', fg='white',font='Time 30', \
                                     selectbackground='green',selectforeground='white', \
                                     exportselection=0,yscrollcommand=scrollbar.set, \
                                     height=5,width=1)
        for i in range(0,60):
            if 0<=i<10:
                self.liste2.insert(i,"0"+str(i))
            else:
                self.liste2.insert(i,str(i))
                
        self.liste2.grid(row=4,column=3,rowspan=4,pady=5,sticky='new')
        scrollbar2.configure(command=self.liste2.yview)
        scrollbar2.grid(row=4,column=4,rowspan=3,pady=5,sticky='nw')
        self.liste2.bind('<<ListboxSelect>>',self.update_minute)

        self.canvas1 = tkinter.Canvas(frame2 ,width=100, height=100, bg='gray25',highlightthickness=0)
        self.canvas1.grid(row=1,column=1)
        self.canvas_image2 = self.canvas1.create_image(0, 0, anchor=NW, \
                                                       image=self.icone_arrosage_off, \
                                                       tags="voyant_off")
             
    def arrosage(self):
    
        self.canvas_image = self.canvas1.create_image(0, 0, anchor=NW, image=self.icone_arrosage_on, \
                                                      tags="voyant_on")
        self.button1.configure(state='disabled')
        os.system('pkill -f gestionnaire_domotique.py')
        proc_arrosage = subprocess.Popen("/home/pi/mdc/arrosage.py", shell=True, \
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc = subprocess.Popen("/home/pi/mdc/gestionnaire_domotique.py", shell=True, \
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.button1.configure(state='normal')
        root.after(duree_arrosage,self.voyant_off)

    def voyant_off(self):
        self.canvas1.delete("voyant_on")
        
    #bug!!! (sortie reste a 1)    
    def stop_arrosage(self):
        os.system('pkill -f arrosage.py')
        GPIO.cleanup()

    def update_jour(self):
        moments_arrosage[6] = self.check_dimanche.get()
        moments_arrosage[0] = self.check_lundi.get()
        moments_arrosage[1] = self.check_mardi.get()
        moments_arrosage[2] = self.check_mercredi.get()
        moments_arrosage[3] = self.check_jeudi.get()
        moments_arrosage[4] = self.check_vendredi.get()
        moments_arrosage[5] = self.check_samedi.get()
        ecriture_fichier()
        update_subprocess()

    def update_heure(self,evt):
        self.hr_arrosage = self.liste.curselection()
        moments_arrosage["hr"] = self.hr_arrosage[0]
        ecriture_fichier()
        update_subprocess()

    def update_minute(self,evt):
        self.min_arrosage = self.liste2.curselection()
        moments_arrosage["min"] = self.min_arrosage[0]
        ecriture_fichier()
        update_subprocess()
                          

    #reste a permettrede changer 1 seul parametre sans avoir
    #a reselectionner tous les autres!
    def initialisation(self):
        with open('/home/pi/mdc/moments_arrosage','rb') as fichier:
            fichier_moments_arrosage = pickle.Unpickler(fichier)
            moments_arrosage_init = fichier_moments_arrosage.load()
            
        self.liste.select_set(moments_arrosage_init["hr"])
        self.liste2.select_set(moments_arrosage_init["min"])
        if moments_arrosage_init[6]==1:self.check_button_dimanche.select()
        if moments_arrosage_init[0]==1:self.check_button_lundi.select()
        if moments_arrosage_init[1]==1:self.check_button_mardi.select()
        if moments_arrosage_init[2]==1:self.check_button_mercredi.select()
        if moments_arrosage_init[3]==1:self.check_button_jeudi.select()
        if moments_arrosage_init[4]==1:self.check_button_vendredi.select()
        if moments_arrosage_init[5]==1:self.check_button_samedi.select()
        indice_dict = ["hr","min",0,1,2,3,4,5,6]
        #set des parametres d'arrosage initiaux
        for i in indice_dict:
            moments_arrosage[i] = moments_arrosage_init[i]
            
        update_subprocess()

    def update(self,evt):
        with open('/home/pi/mdc/event_arrosage','rb') as fichier:
            fichier_event_arrosage = pickle.Unpickler(fichier)
            event_arrosage = fichier_event_arrosage.load()
            self.dernier_arrosage.set(event_arrosage["date_dernier_arrosage"])
            self.dernier_arrosage_hr.set(event_arrosage["heure_dernier_arrosage"])
            self.dernier_arrosage_etat.set(event_arrosage["etat_arrosage"])
                     
try: 
    root = tkinter.Tk()
    root.wm_title('Master Domotic Control')
    root.geometry('600x1000+0+0')
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", arret)
    app.initialisation()
    root.mainloop()
    
##    while True:
##        #Equivalent de root.mainloop()
##        root.update_idletasks()
##        root.update()
    
except(KeyboardInterrupt, SystemExit):
    arret()
    






    
