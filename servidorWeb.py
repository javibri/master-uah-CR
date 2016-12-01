from flask import Flask
from flask import render_template
import json
from bson import json_util
from flask import request
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__, static_url_path='')

client = MongoClient('localhost', 27017)
db = client.bolsa
collection = db['datos']
datos_reales=collection.find().sort([( '_id' , -1 )] ).limit(1).next()


@app.route('/')
def nada():
  datos_reales=collection.find().sort([( '_id' , -1 )] ).limit(1).next()
  return render_template('index.html', valor=datos_reales['valor'], fecha=datos_reales['fecha'], hora=datos_reales['hora'])
  


@app.route('/index.html')
def index():
  datos_reales=collection.find().sort([( '_id' , -1 )] ).limit(1).next()
  return render_template('index.html', valor=datos_reales['valor'], fecha=datos_reales['fecha'], hora=datos_reales['hora'])
  


@app.route('/getDatosBolsa')
def getDatosBolsa():
	to_return = []
	for document in collection.find():
		print document['_id']	
		to_return.append(document)
	return json.dumps(to_return, default=json_util.default)



@app.route('/UltimoDato')
def UltimoDato():
	for document in collection.find():
	  return json.dumps(collection.find().sort([( '_id' , -1 )] ).limit(1).next(), default=json_util.default)
       


@app.route('/Prueba')
def prueba():
  datos_reales=collection.find().sort([( '_id' , -1 )] ).limit(1).next()

  primerv=db.datos.find({},{"_id":0,"hora":0,"fecha":0}).limit(1)
  return json.dumps(primerv)
    
    
    
@app.route('/Media')   
def Media():
  valores=collection.find()
  valores = [ float(x['valor'].replace(',','.')) for x in valores]
  media = sum(valores) / len(valores)
  return json.dumps(media)



@app.route('/media.html')   
def MediaHTML():
  valores=collection.find()
  valores = [ float(x['valor'].replace(',','.')) for x in valores]
  media = sum(valores) / len(valores)
  return render_template('media.html', media=media, fecha=datos_reales['fecha'])



@app.route('/umbral.html',methods=['GET'])
def umbral():
  flag=0
  datos_reales=collection.find().sort([( '_id' , -1 )] ).limit(1).next()
  valor_ini=db.datos.find().limit(1).next()
  valor_ini=float(valor_ini['valor'].replace(',','.'))
  valor_actual=float(datos_reales['valor'])
  umbral_introducido = float(request.args.get('nombre'))
  umbral = umbral_introducido * valor_ini / 100
  valor_deteccion = valor_ini + umbral
  if valor_actual>valor_deteccion:
    flag=1
  return render_template('umbral.html', valor=datos_reales['valor'], fecha=datos_reales['fecha'], hora=datos_reales['hora'],umbral=valor_deteccion, ppp=str(umbral_introducido), umbral_introducido=umbral_introducido , valor_ini=valor_ini, flag=flag)  



@app.route('/umbral2.html',methods=['GET'])
def umbral2():
  flag=0
  datos_reales=collection.find().sort([( '_id' , -1 )] ).limit(1).next()
  valor_actual=float(datos_reales['valor'])
  umbral_introducido = float(request.args.get('umbral2'))
  valor_ini = float(request.args.get('valor_umbral'))
  umbral = umbral_introducido * valor_ini / 100
  valor_deteccion = valor_ini + umbral
  if valor_actual>valor_deteccion:
    flag=1
  return render_template('umbral2.html', valor=datos_reales['valor'], fecha=datos_reales['fecha'], hora=datos_reales['hora'],umbral=valor_deteccion, ppp=str(umbral_introducido), umbral_introducido=umbral_introducido , valor_ini=valor_ini, flag=flag)
  
  

@app.route('/zona_privada.html')
def zona_privada():
  datos_reales=collection.find().sort([( '_id' , -1 )] ).limit(1).next()
  valores=collection.find()
  valores = [ float(x['valor'].replace(',','.')) for x in valores]
  media = sum(valores) / len(valores)
  return render_template('zona_privada.html', valor=datos_reales['valor'], fecha=datos_reales['fecha'], hora=datos_reales['hora'], media=media)



if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0')
