import sys
import time
import pymongo
import BeautifulSoup
import re
import urllib2
from time import strftime
from datetime import datetime

MONGO_SERVER = "127.0.0.1"
MONGO_DATABASE = "wikis"
MONGO_COLLECTION = "wikiCollectionCapped"
MONGO_COLLECTION_OUT = "vandalResults"
# MONGO_DATABASE = "wikis"
# MONGO_COLLECTION = "newWikisCapped"
# MONGO_COLLECTION_OUT = "testOutput"

#defining what is a newline, for scraper
Newlines = re.compile(r'[\r\n]\s+')
#connect to db and wikiCollection
mongodb = pymongo.Connection(MONGO_SERVER, 27017)
database = mongodb[MONGO_DATABASE]
collection = database[MONGO_COLLECTION]
collection_out = database[MONGO_COLLECTION_OUT]

#get a cursor to loop through documents by time
cursor = collection.find({'scraped': {'$ne': 1}}, await_data=True, tailable=True)

#lets check to see it worked
try:
	while cursor.alive:
		#print "Start"
		
		#check if record has been processed already
		#if cursor.next({'scraped': {'$ne': 1}}):
			#if so, scrape it
		try:
			message = cursor.next()
			
			#date = datetime.fromtimestamp(int(message['time'])).strftime('%Y-%m-%d %H:%M:%S')

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
			
			soup = BeautifulSoup.BeautifulSoup(data)
			soup2 = BeautifulSoup.BeautifulSoup(data, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
			
			#for now only give us the deletions of vandalism on not the vandalistic delections
			#if message['delta'] < 0:
				##scrape that url and get the diff text
				#txt = soup.find('td', {'class':'diff-deletedline'}).getText('\n')
			try:
				#TODO 25JUN2012 - fix this scraping business here
				
				offender = soup2.find('a', {'class':'mw-userlink'}).getText()
			
				#txt = [td.find('span', {'class':'diffchange diffchange-inline'}).getText('\n') for td in soup.findAll('td', {'class':'diff-deletedline'})]
				txt = [td.findAll('div') for td in soup.findAll('td', {'class':'diff-deletedline'})]
				txt2 = [td.findAll('div') for td in soup.findAll('td', {'class':'diff-addedline'})]		
				nest = [td.find('img') for td in soup.findAll('a', { 'class': 'image'} )]
				imgs = [x['src'] for x in nest]
				if len(imgs)>0:
					img = "http:" + imgs[0]
				else:
					img = "no image"
				
				if re.match(r"\d+.\d+.\d+.\d+", offender):
					anon = True
				else:
					anon = False 

				txt = str(txt).strip('[[]]')				
				txt2 = str(txt2).strip('[[]]')
				#txt = txt.string
				#txt2 = txt2.string

				print txt
				print txt2
				print '===',message['page'],'==='
				#print vandal_text
				print img
				#time.sleep(10)

			except AttributeError as e:
				print 'something wrong with the text', e
				txt = "This vandalism is not available right now."
				print txt
				continue
			#else:
				#print '===',message['page'],'==='
				#print 'Not a deletion'
				#txt = 'Not a deletion'
				#nest = [td.find('img') for td in soup.findAll('a', { 'class': 'image'} )]
				#imgs = [x['src'] for x in nest]
				#if len(imgs)>0:
				#	img = "http:" + imgs[0]
				#else:
				#	img = "no image"
	
			collection_out.insert({'time':message['time'],
								   'date':message['date'],
								   'date_str': message['date2'],
								   'diff_url':message['url'], 
								   'page':message['page'], 
								   'vandalism':txt,
								   'unvandalism':txt2,
								   'offender':offender,
								   'reverter': message['user'], 
								   'image':img,
								   'anon': anon,
								   'delta':message['delta']})
			
			#use this opportunity to update the input record
			collection.update({"_id":message['_id']}, {'$set':{'scraped': 1}}, upsert=True)
			
		except StopIteration:
			print "No more records"
			sys.exit(0)
		#if not, move on to next record
		#else:
			# print "arready screpped"
			# pass
				
except pymongo.errors.OperationFailure as e:
	print "Utterly failed, this is so bad. What happened was: ", e
	
except KeyboardInterrupt:
	print "CONTROL-C'd!"
	sys.exit(0)

print "bye-bye!"	



