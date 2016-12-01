#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import re
import pymongo
import time

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.bolsa
collection = db['datos']

while(True):
  try:
    to_wait = -(time.time()%300) + 300
    time.sleep(to_wait)
    response = urllib2.urlopen('http://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000')
    
    # Get all data
    html = response.read()
    #print "Get all data: ", html
    
    tabla = re.search( '<table class="TblPort" cellspacing="0" cellpadding="3" border="0" id="ctl00_Contenido_tblAcciones"(.|\n)*?</table>', html).group(0)
    acciona = re.search( 'ACCIONA</a>.*</td>', tabla).group(0)
    bus_td = re.search( '<td>.*</td>', acciona).group(0)
    bus_td2 = re.sub( '<td>|</td>', '',bus_td)
    bus_td = bus_td.replace(',', '.')
    
    #print tabla
    print '-----------VALOR-------------------'
    valor = re.search( '([0-9]{1,8}\.[0-9]{1,8})',bus_td).group(0)
    print valor 
    
    print '-----------FECHA-------------------'
    fecha = re.search( '([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,4})',bus_td).group(0)
    print fecha
    
    print '-----------HORA---------------------'
    hora = re.search( '([0-9]{1,2}\:[0-9]{1,2})',bus_td).group(1)
    print hora
    
    collection.insert_one({'valor':valor, 'fecha':fecha, 'hora':hora})
    
    print('Thingspeak pre')
    urllib2.urlopen('https://api.thingspeak.com/update?api_key=RYEK7OLBHL3P3W1F&field1='+ str(valor))
    print('Thingspeak post')

  except:
    pass