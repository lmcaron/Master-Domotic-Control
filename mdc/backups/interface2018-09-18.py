#!/usr/bin/python3
#Interface du Master Domotic Control
import tkinter
from tkinter import *
import math
import os

class App:
    
    def __init__(self, master): #double underscore
        #Paramètre self permet de contenir toutes les variables (attributs, méthodes) propres à la classe
        frame1 = tkinter.Frame(master)#objet frame encapsulé dans l'objet root de classe App
        frame1.pack(fill=tkinter.BOTH, expand=1)#la couleur va remoplir toute la fenetre lorsque redimensionné
        frame1.configure(background='gray25')
        #height 1: une ligne de cette font entre dans le label        
        #tkinter.Label(frame1, text='Master Domotic Control',bg='gray25',fg='white',font='Time 35',height=1).grid(row=0,column=0)
        tkinter.Label(frame1, text='Master Domotic Control',bg='gray25',fg='white',font='Time 35',height=1).pack() 
        """
        self.c_var = tkinter.DoubleVar()#Attribut c_var dans classe App
        tkinter.Entry(frame, textvariable=self.c_var, font='20').grid(row=4,column=1)
        
        self.result_var = tkinter.DoubleVar()
        tkinter.Label(frame, textvariable=self.result_var,bg='gray25',fg='white',font='20').grid(row=0,column=3,columnspan=2)
        tkinter.Label(frame, text='rad',bg='gray25',fg='white',font='20').grid(row=0,column=5)

        """
        self.icone_arrosage1 = PhotoImage(file='/home/pi/mdc/icone_arrosage.png')
        self.icone_arrosage = self.icone_arrosage1.subsample(15,15)

        
        frame2 = tkinter.LabelFrame(frame1, text='Arrosage', borderwidth=4,
                                    bg='gray25', fg='white', font='Time 15', padx=20, pady=20)
        frame2.pack(fill='both')

        label1 = tkinter.Label(frame2, text='Arrosage manuel des plantes',
                               bg='gray25', fg='white',font='Time 18',height=1)
        label1.grid(row=0,column=1, pady=20)

        button2 = tkinter.Button(frame2, command=self.arrosage) 
        button2.grid(row=0,column=0, padx=20, pady=20, sticky='n')
        button2.configure(image=self.icone_arrosage, compound='center')
        
        #self.check_var = tkinter.StringVar()
        #button2 = tkinter.Checkbutton(frame, text='option1',variable=self.check_var,
        #                              onvalue='Y', offvalue='N',bg='gray25',fg='white',font='20')
        #button2.grid(row=3,column=0)
        
    #ajouter commande anti rebond pour éviter de lancer une série de commandes non voulue.
    def arrosage(self):
        os.system('python3 /home/pi/codes/test_output_exe.py')


root = tkinter.Tk()
root.wm_title('Master Domotic Control')
root.geometry('600x800+0+0')
app = App(root)

root.mainloop()


    
