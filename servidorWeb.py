from flask import Flask
import json
from bson import json_util

app = Flask(__name__, static_url_path='')

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.cotizacion_bolsa
collection = db['datos_cotizacion']

@app.route('/')
def index():
	return 'hola mundo'
	return app.send_static_file('index.html')

@app.route('/hola')
def index1():
	return app.send_static_file('index.html')

@app.route('/getDatosBolsa')
def getDatosBolsa():
	to_return = []
	for document in collection.find():
		print document['_id']
		if 'ACERINOX' in document:
			print document['ACERINOX']
		to_return.append(document)
	return json.dumps(to_return, default=json_util.default)


if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0')
