#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dryscrape
import re

### Coger el contenido de la pagina.
url = 'http://www.elmundo.es/economia/bolsa/indices/ibex35_I.IB.html'
session = dryscrape.Session()
session.visit(url)
html = session.body()

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
    organizacion    = organizacion.encode('utf-8')
    valor           = re.sub( '(<td.*?>)|(</td>)', '', valores[1])
    valor           = valor.replace(',', '.')
    valor           = float(valor)
    datosRe[ organizacion ] = valor

print '-------------  Regex  -------------'
print datosRe
