import sys
import time
import pymongo
import BeautifulSoup

MONGO_SERVER = "127.0.0.1"
MONGO_DATABASE = "wikis"
MONGO_COLLECTION = "wikiCollectionCapped"


#connect to db and wikiCollection
mongodb = pymongo.Connection(MONGO_SERVER, 27017)
database = mongodb[MONGO_DATABASE]
collection = database[MONGO_COLLECTION]

#get a cursor to loop through documents by time
cursor = collection.find({}, await_data=True, tailable=True)

#lets check to see it worked
try:
	while cursor.alive:
		print "Start"
		try:
			message = cursor.next()
			print message
		except StopIteration:
			print "Something happened with our cursor test :("
			time.sleep(1)
except pymongo.errors.OperationFailure:
	print "Utterly failed, this is so like you."
	
except KeyboardInterrupt:
	print "CONTROL-C, NOOOO!"
	sys.exit(0)

print "bye-bye!"	

##get url from each documents

##scrape that url and get the diff text

##save diff text

##update to include text with each documents

##repeat
