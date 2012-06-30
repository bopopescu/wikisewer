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

@app.route('/less')
def less_page():
	#vandalism = mongo.db.vandalResults.find()
	vandalism_less = vandalisms.find({'delta': {'$lt':50}})
	return render_template('less.html', vandalism_less = vandalism_less)

@app.route('/images')
def less_page():
	#vandalism = mongo.db.vandalResults.find()
	vandalism_img = vandalisms.find({'image': {'$ne':'no image'}})
	return render_template('images.html', vandalism_img = vandalism_img)

if __name__ == '__main__':
	app.run()