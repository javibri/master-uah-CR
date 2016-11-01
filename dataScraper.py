#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dryscrape
import re
import pymongo
import time

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.cotizacion_bolsa
collection = db['datos_cotizacion']

### Coger el contenido de la pagina.
url = 'http://www.elmundo.es/economia/bolsa/indices/ibex35_I.IB.html'

"""
### La menara que no te gusta.
import BeautifulSoup
datosSoup = {}

soup = BeautifulSoup.BeautifulSoup(html)
table = soup.find( 'table', {'id':'listado_valores'} ).find('tbody')
filas = table.findAll("tr")
for fila in filas:
    valores = fila.findAll('td')
    organizacion    = valores[0].getText().encode('utf-8')
    valor           = float(valores[1].getText().replace(',', '.'))
    datosSoup[ organizacion ] = valor

print '-------------  BeatifulSoup  -------------'
print datosSoup
"""

while(True):
	try:
		to_wait = -time.time()%120 + 120
		print '1'
		time.sleep(to_wait)
		print '2'
		session = dryscrape.Session()
		session.visit(url)
		html = session.body()
		print '3'

		### La manera que te gusta
		datosRe = {}
		tabla = re.search( '<table id="listado_valores",*?>(.|\n)*?</table>', html).group(0)
		tbody = re.search( '<tbody>(.|\n)*?</tbody>', tabla).group(0)
		filas = re.findall(   '<tr.*?>.*?</tr>', tbody)
		print '----------------------------------'
		for fila in filas:
		    valores = re.findall( '<td.*?>.*?</td>', fila)
		    organizacion    = re.sub( '(<td.*?>)|(</td>)', '', valores[0])
		    organizacion    = re.sub( '(<a.*?>)|(</a>)', '', organizacion)
		    organizacion    = re.sub( '\.', '', organizacion)
		    organizacion    = organizacion.encode('utf-8')
		    valor           = re.sub( '(<td.*?>)|(</td>)', '', valores[1])
		    valor           = valor.replace(',', '.')
		    valor           = float(valor)
		    datosRe[ organizacion ] = valor

		print '-------------  Regex  -------------'
		print datosRe
		collection.insert_one(datosRe)
	except:
		pass
