import telebot
import time
import MySQLdb
import serial
import requests
import socket
from time import sleep
import picamera
from subprocess import call
import random
from os import remove
from ftplib  import  FTP
import os
from datetime import date
from datetime import datetime
import serial
from numpy import *
import matplotlib.pyplot as plt
from pylab import *
from ftplib  import  FTP
import os
from datetime import datetime
import random

#aqui crearemos un script  de condicions de si o no hay internet para enviar las foto termica al servidor , si en caso no ubiera se tomara la foto y se cargara a una carpeta a la espera 
#de conexion a internet
global  now


now = datetime.now()

#con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#habrimos nuestro bot 
#       943769984:AAGOjMs0T4Vu9-fuGzUcZ1fVU3YQctbupAE"
bot = telebot.TeleBot("943769984:AAGOjMs0T4Vu9-fuGzUcZ1fVU3YQctbupAE")

chat_id="1051367732"



conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#intenta conectarse a una url con el socket creado
try:
# si existe conexion a internet   se ejecutara lo siguiente 
    conn.connect(('www.raspberrypi.org', 80))


    os.system('python /home/pi/termica/foto-termica.py')

    servidor="ftp.soft.pe"
    user="polines@polines.soft.pe"
    passw="innova_polines"


     # donde queremos subir el fichero
    ftp_raiz     = '/public/img/fotos_termica/'

#    fichero_origen='/home/pi/termica/imagen.jpg'
    fichero_origen='/home/pi/termica/termica.png'
#    now = datetime.now()
    #now = datetime.now()
    nom = (str(now)+'.png')
    fichero_termica=('_'.join(nom.split()))

    try:

#	bot.send_message(chat_id,'....BIENVENIDO AL BOT LOS PINPOLLOS ....')
	photo = open('/home/pi/termica/termica.png', 'rb')
        bot.send_photo(chat_id, photo)
	
	print "entro aqui"
        s=FTP(servidor)
        s.login(user, passw)


        try:
            f = open(fichero_origen, 'rb')
            s.cwd(ftp_raiz)
            s.storbinary('STOR ' + fichero_termica, f)
	    f.close()
            s.quit()
            print  "enviada la foto  termica al hosting"
	except:
            print "no se envio la foto al hosting"
    except :

        bot.send_message(chat_id, "Fallo al  arrancar la camara termica, prueba mas tarde por favor")
#    conn.close()

except:
#si no hay internet ejecutara lo siguiente

    import serial
    from numpy import *
    import matplotlib.pyplot as plt
    from pylab import *
    import numpy as np
    from datetime import date
    from datetime import datetime


#    now = datetime.now()
    nom = (str(now)+'.png')
    fichero_termica=('_'.join(nom.split()))


    today = date.today()

    ser = serial.Serial('/dev/ttyACM0',9600)
#ser = serial.Serial('/dev/ttyUSB0') 
    read = 0
    element = 0
    counter = 0

    w, h = 8, 8;
    Matrix = [[0 for x in range(w)] for y in range(h)]

    x = 0;
    y = 0;


#    os.system('python /home/pi/termica/foto-termica2.py')
    #now = datetime.now()
    while True:
    	    while True:
	            char = ser.read()

       		    if read==1:
                  	    if char==",":

                                    Matrix[x][y]=element
                                    x=x+1
                                    element = 0
                                    counter = 0
                                    ser.read()
                            elif ord(char)==13:
                                    y=y+1
                                    x=0
                                    element = 0
                                    counter = 0
                                    ser.read()
                            elif char == "]":
                                    read=0

#                               print Matrix
                                #print "Done"
                                    x=0
                                    y=0
                                    break
            	            elif char!=".":

#                               print element
                                    element = element + int(char)*pow(10, 1-counter)
                                    counter = counter+1
#                               print  counter
                    if char == "[":
                            read=1


            matriz = np.array( Matrix)
            plt.figure()
            conf_arr = np.array(Matrix)
            plt.matshow(conf_arr,cmap = plt.get_cmap('jet'),interpolation='nearest')
            plt.colorbar()
            plt.title(today.strftime("%B %d, %Y"+'\n' + time.strftime("%X") +'\n' ))
            plt.xlabel(matriz[4::].max(), family='serif', color='r', weight='normal',size = 16,labelpad = 6)
            plt.savefig('/home/pi/termica/fotos/'+fichero_termica, format='png')
            plt.show()
            print "ejecutado camara termica de arduino puerto serial"
            break
	    sys.exit()
    #break
	 #   conn.close()
conn.close()

