from flask import Flask, render_template
#from mongokit import Connection, Document
#from flask.ext.pymongo import PyMongo
from pymongo import Connection#, json_util
 	

#MONGO_HOST = 'localhost'
#MONGO_PORT = 27017

app = Flask(__name__)
connection = Connection()
db = connection.wikis
vandalisms = db.vandalResults
#mongo = PyMongo(app)
#app.config.from_object(__name__)
app.debug = True

#connection = Connection(app.config['MONGO_HOST'],
						#app.config['MONGO_PORT'])
@app.route('/')
def home_page():
	#vandalism = mongo.db.vandalResults.find()
	vandalism = vandalisms.find()
	return render_template('index.html', vandalism = vandalism)

if __name__ == '__main__':
	app.run()