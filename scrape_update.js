//import nodeio for scraping and mongodb for connecting to on and saving to another mongo collection

var nodeio = require('node.io'),
	mongo = require('mongodb'),
		db = new mongo.Db('wikis', new mongo.Server('localhost', 27017, {}), {});

//connect to db and wikiCollection


//loop through documents by time

////get url from each documents

////scrape that url and get the diff text

////save diff text

////update to include text with each documents

////repeat