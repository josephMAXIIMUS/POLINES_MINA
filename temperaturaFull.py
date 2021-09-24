import telebot
import requests
import socket
from time import sleep
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
import sys
import smbus
import os
import json
import requests, json
from json.decoder import JSONDecoder


#definimos una funcion temperatura para poder llamar a alas variables que  tempeturamaxima y minima desde una api en php 
def temperaturas():
    global TemperaturaMaxima
    global TemperaturaMinima
    


    con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#intenta conectarse a una url con el socket creado
    try:
    	con.connect(('www.emusapabancay.com.pe', 80))
	#recuperando valores de la url
        url = requests.get("https://polines.soft.pe/public/api/parametros")
        text = url.text
        data = json.loads(text)
        separador=data['valores']
        maximo=float(separador['maximo'])
        minimo=float(separador['minimo'])
        TemperaturaMaxima=maximo
        TemperaturaMinima=minimo
    except:
	#asignamos las medidas para el caso que no ubiera internet 
	TemperaturaMaxima= 40
	TemperaturaMinima= 30
    #cierra el conector
    con.close()

#definimos una funcion alerta para enviar las notificaicones al telegram 
def alerta(TemperaturaAmbiente, TemperaturaObjeto):
    con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #intenta conectarse a una url con el socket creado
    try:
        con.connect(('www.emusapabancay.com.pe', 80))
	#llamamos a nuestro bot creado 
        bot = telebot.TeleBot("943769984:AAGOjMs0T4Vu9-fuGzUcZ1fVU3YQctbupAE")
    	#bot = telebot.TeleBot("g540124023")
	#este es nuestro id del numero de telegram a quien le llegara las notificaciones 
    	chat_id="1051367732"
    	mensaje1=bot.send_message(chat_id ,"ESTA ES UNA NUEVA ALERTA DE TEMPERATURA DEL POLIN NUMERO -1-")
    	mensaje1=bot.send_message(chat_id ,"LA TEMPERATURA AMBIENTE SE ENCUANTRA EN  == "+ str(TemperaturaAmbiente))
    	mensaje2 =bot.send_message(chat_id," LA  TEMPERATURA DEL  OBEJETO  PASO LOS PARAMETRSO ESTABLECIDOS == "+ str (TemperaturaObjeto))
	con.close()

    except:

	print "no hay se envio alerta"


#definimos  una funcion gmail la cual sera la que nos enviara las notificiones al Gmail 
def gmail(Tobjeto,Tambiente):
    con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    try:
        con.connect(('www.emusapabancay.com.pe', 80))

    	import smtplib
    	from_addr = 'milquiann@gmail.com'
    	to = '151145@unamba.edu.pe'
    	message = ('no te preocupes sigue funcionando las alertas  OBJETO' + str(Tobjeto)+ '/AMBIENTE'+ str(Tambiente))

    # Reemplaza estos valores con tus credenciales de Google Mail
    	username = 'milquiann@gmail.com'
    	password = 'mamimelchorita3'

    	server = smtplib.SMTP('smtp.gmail.com:587')
    	server.starttls()
    	server.login(username, password)
    	server.sendmail(from_addr, to, message)

    	server.quit()
	con.close()

    except:
        print "no hay se envio gmail"


#creamos una funcion  CSV  la cual se encargara de almacenar los datos de las lecturas  de los sensores y demas , todo esto se almacenara en un archivo csv llamado data.csv
def csv(sensor,Tobjeto,Tambiente,valor,fichero_foto,fichero__termica):
    import csv
    from datetime import datetime

    temperaturaAmbiente = float (Tambiente)
    temperaturaObjeto = float (Tobjeto)
    sensor =str (sensor)
 
    fecha =datetime.now()
    fecha= str(fecha)
    id_local = 1
    id_nivel= valor
    created_at = datetime.now()
    updated_at = datetime.now()
    #totalDatos = [sensor,fecha,temperauraObjeto,temperaturaAmbiente,valor,fichero_foto,fichero__termica]
    totalDatos = (id_local,id_nivel,temperaturaObjeto,temperaturaAmbiente,fecha,fichero_termica,fichero_foto,sensor,created_at,updated_at)
    with open("/home/pi/termica//datas.csv","a") as f:
        cr = csv.writer(f,delimiter=",",lineterminator= "\n")
        cr.writerow(totalDatos)



if __name__ == "__main__":

#importamos o llamamos  a nuestro archivo  llaamdo temp.py, el cual nos devolvera las variables TemperaturaAmbiente y TemperaturaObjeto
    from temp import  *
    TemperaturaAmbiente= TemperaturaAmbiente #llamamos a la variable del archvo temp.py
    TemperaturaObjeto= TemperaturaObjeto #llamamos a la variable del archvo temp.py

    temperaturas()    #llamamos a la funcion tempeteratura para capturar los datos  del internet o estaticos

#crearemos las condicionales  para poder controlar  el maximo , minimo y normal de temperatura , segun cada caso se ejecutara una serue de comandos 
	#si la temperatura - no pase de los parametros sera normal  y solo se guardara las lecturas pero no ninguna imagen 
    if((TemperaturaObjeto >  TemperaturaMinima and TemperaturaObjeto < TemperaturaMaxima)):
        print TemperaturaObjeto
        print TemperaturaAmbiente
	print  TemperaturaMaxima
        print  TemperaturaMinima 
        print "se ejecutado la condicion  de temperatura normal"
        valor=1
	sensor=1
        fichero_foto = "null"
        fichero_termica = "null"
        #ejecutamos la funcion csv
	csv(sensor,TemperaturaObjeto,TemperaturaAmbiente,valor,fichero_foto,fichero_termica)
 
        #si la temperatura - no pasa de los parametros sera mayor  , en este caso se guardara las imagenes  foto y  termografo y los daos delos sensores 

    if( TemperaturaObjeto > TemperaturaMaxima):
        print TemperaturaObjeto
        print TemperaturaAmbiente
        print  TemperaturaMaxima
        print  TemperaturaMinima
	print "se ejecuto la condicion  de temperatura mayor"
	valor=3
	sensor=1

        alerta(TemperaturaObjeto,TemperaturaAmbiente)
        gmail(TemperaturaObjeto,TemperaturaAmbiente)
	#importamos  el archivo sms.py el cual ejecuta el envio de un mensaje de texto 
	from sms import  *
	#ejecutamos el archivo  termicai.py y obtemos la varaible -fichero_termica
        from termicai import fichero_termica
	time.sleep(5)
	#improtamos  el archivo fotoi.py y obtenemos la variable fichero_foto
        from fotoi import fichero_foto
	time.sleep(2)
	#llamamos ala funcion csv
        csv(sensor,TemperaturaObjeto,TemperaturaAmbiente,valor,fichero_foto,fichero_termica)
#        gmail(TemperaturaObjeto,TemperaturaAmbiente)
	time.sleep(2)
	#ejecutamos  FotoFTP.py' y TermicaFTP.py' los cuales envia los datos al servidor segun la conexion de datos (internet)
	os.system('python /home/pi/termica/FotoFTP.py')
	time.sleep(2)
        os.system('python /home/pi/termica/TermicaFTP.py')
	

        #si la temperatura - si la lectura es muy baja  entonces sera menor   y solo se guardara las lecturas pero no ninguna imagen

    if( TemperaturaObjeto < TemperaturaMinima):
        print TemperaturaObjeto
        print TemperaturaAmbiente
        print  TemperaturaMaxima
        print  TemperaturaMinima
        print "se ejecuto la condicion  de temperatura menor"
        valor=2
	sensor=1
        fichero_foto = "null"
        fichero_termica = "null"
	#ejecutamos la funcion csv 
        csv(sensor,TemperaturaObjeto,TemperaturaAmbiente,valor,fichero_foto,fichero_termica)

