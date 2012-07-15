from flask import Flask, render_template, request, redirect, flash
#from mongokit import Connection, Document
#from flask.ext.pymongo import PyMongo
from pymongo import Connection#, json_util
#from pymongo.objectid import ObjectId #this is deprecated
import bson.objectid
 	

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
	
	#flash('you guys have all the fun!')
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

#increment a vote
@app.route('/vote_up/<this_record>')
def vote_up(this_record):

	#this_item = vandalisms.find({'_id':bson.objectid.ObjectId(this_record)})

	vandalisms.update({'_id':bson.objectid.ObjectId(this_record)}, 
					  {"$inc" : { "votes": 1 }}, upsert=True)
	return redirect("/")


#how to add tags
@app.route('/tagger/<thisguy>')
def tag_it(thisguy):
	
	#TODO - This tags item is the problem, look into request form get>oo<
	
	#tags = request.form.get('tag', [])
	tags = request.form.getlist('tag', [])
	
	print type(tags)
	print tags


	#this_item = vandalisms.find({'_id': bson.objectid.ObjectId(thisguy)})

	print this_item[1]


	vandalisms.update({'_id': bson.objectid.ObjectId(thisguy)},
					  {'$pushAll': {'tags': tags}}, upsert=True)
	#flash('New tag added')

	return redirect("/")


if __name__ == '__main__':
	app.run()