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
			#for now only give us the deletions of vandalism on not the vandalistic delections
			if message['delta'] < 0:
				##scrape that url and get the diff text
				#txt = soup.find('td', {'class':'diff-deletedline'}).getText('\n')
				try:
					txt = [td.find('span', {'class':'diffchange diffchange-inline'}).getText('\n') for td in soup.findAll('td', {'class':'diff-deletedline'})]
					nest = [td.find('img') for td in soup.findAll('a', { 'class': 'image'} )]
					img = [x['src'] for x in nest]

				
					print '===',message['page'],'==='
					print txt
					print img
					#time.sleep(10)
				except AttributeError as e:
					print 'something wrong with the text', e
					continue
			else:
				print '===',message['page'],'==='
				print 'Not a deletion'
	

			
		except StopIteration:
			print "No more records"
			sys.exit(0)
			
except pymongo.errors.OperationFailure as e:
	print "Utterly failed, this is so bad. What happened was: ", e
	
except KeyboardInterrupt:
	print "CONTROL-C'd!"
	sys.exit(0)

print "bye-bye!"	




##save diff text

##update to include text with each documents

##repeat
