import sys
import time
import pymongo
import BeautifulSoup
import re
import urllib2

MONGO_SERVER = "127.0.0.1"
MONGO_DATABASE = "wikis"
MONGO_COLLECTION = "wikiCollectionCapped"

#defining what is a newline, for scraper
Newlines = re.compile(r'[\r\n]\s+')
#connect to db and wikiCollection
mongodb = pymongo.Connection(MONGO_SERVER, 27017)
database = mongodb[MONGO_DATABASE]
collection = database[MONGO_COLLECTION]

#get a cursor to loop through documents by time
cursor = collection.find({}, await_data=True, tailable=True)

#lets check to see it worked
try:
	while cursor.alive:
		#print "Start"
		try:
			message = cursor.next()
			#print the entire record
			#print message
			#print the URL only
			#this is what we will scrape
			##get url from each documents
			url = message['url']
			print "Now scraping: ", message['url']

			#try:
			req = urllib2.Request(url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5'})
			data = urllib2.urlopen(req).read()
			soup = BeautifulSoup.BeautifulSoup(data, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
			if message['delta'] < 0:
				txt = soup.find('td', {'class':'diff-deletedline'}).getText('\n')
				#.find('span', {'class':'diffchange diffchange-inline'})
				print txt
			else:
				print 'Not a deletion'
			#except Error as e:
				

			
		except StopIteration:
			#print "Something happened with our cursor test :("
			time.sleep(1)
except pymongo.errors.OperationFailure:
	print "Utterly failed, this is so bad."
	
except KeyboardInterrupt:
	print "CONTROL-C'd!"
	sys.exit(0)

print "bye-bye!"	


##scrape that url and get the diff text

##save diff text

##update to include text with each documents

##repeat
