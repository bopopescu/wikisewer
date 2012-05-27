//imports

var fs = require('fs'),
	path = require('path'),
	irc = require('irc-js'),
	nodeio = require('node.io'),
	//redis = require('redis').createClient();
	mongo = require('mongodb'),
		db = new mongo.Db('wikis', new mongo.Server('localhost', 27017, {}), {});

function listen(config, callback){
	channels = [];
	for (var channel in config.wikipedias){ 
		channels.push(channel);
	}

	var client = new irc({
		server: 'irc.wikimedia.org',
		nick: config.ircNick,
		log: config.log,
		user: {
			username: config.ircUserName,
			realname: config.ircRealName
		}
	});

	client.connect(function(){
		client.join(channels);
		client.on('privmsg', function(msg){
			m = parse_msg(msg.params, config);
			if (m){
				callback(m);
				saveRecs(m);
			}
		});
	});

}

function parse_msg(msg, config){
	//this regex is fairly impenetrable
	//need to come back to this and figure out what it's doing

	var m = /\x0314\[\[\x0307(.+?)\x0314\]\]\x034 (.*?)\x0310.*\x0302(.*?)\x03.+\x0303(.+?)\x03.+\x03 (.*) \x0310(.*)\x03?.*/.exec(msg[1]);
	if (! m){
		console.log("could not parse: " + msg);
		return null;
	}

	//number of characters edited - to int
	if (m[5]) {
		var delta = parseInt(/([+-]\d+)/.exec(m[5])[1]);

	} else {
		var delta = null;
	}

	//anonymous edit check
	var user = m[4];
	//if user is any ip address, it's anonymous
	var anonymous = user.match(/\d+.\d+.\d+.\d+/) ? true : false;

	//parsing flags
	var flag = m[2];
	var isRobot = flag.match(/B/) ? true:false;
	var isNewPage = flag.match(/N/) ? true:false;
	var isUnpatrolled = flag.match(/!/) ? true:false;
	var isMinor = flag.match(/M/) ? true:false;
	var page = m[1];
	var wikipedia = msg[0];
	var wikipediaUrl = 'http://' + wikipedia.replace('#', '') + '.org';
	var pageUrl = wikipediaUrl + '/wiki/' + page.replace(/ /g, '_');
	var userUrl = wikipediaUrl + '/wiki/User:' + user;
	var namespace = getNamespace(wikipedia, page, config);
	var vandalContent;
	

	//from https://github.com/chriso/node.io
	//I get the feeling this is not going to work.
	// if (m[6].match(/vandal/) && namespace === "article"){
	// 	nodeio.scrape(function(){
	// 		this.getHtml(m[3], function(err, $){
	// 			//console.log('getting HTML, boss.');
	// 			console.log(err);
	// 			var output = [];
	// 			$('span.diffchange.diffchange-inline').each(function(scraped){
	// 				output.push(scraped.rawtext);
	// 			});
	// 			vandalContent = output.toString();
	// 			console.log("your content is: " + vandalContent);

	// 		  });

	// 		});
	// 	} else {
	// 		vandalContent = "no content";
	// 	}
	
 
	return {
		flag: flag,
		page: page,
		pageUrl: pageUrl,
		url: m[3],
		delta: delta,
		comment: m[6],
		wikipedia: wikipedia,
		wikipediaUrl: wikipediaUrl,
		wikipediaShort: config.wikipedias[msg[0]].short,
		wikipediaLong: config.wikipedias[msg[0]].long,
		user: user,
		userUrl: userUrl,
		unpatrolled: isUnpatrolled,
		anonymous: anonymous,
		robot: isRobot,
		namespace: namespace,
		minor: isMinor
		//vandalContent: vandalContent
	}
	
}


function getNamespace(wikipedia, page, config){
	ns = null;
	var parts = page.split(':');
	if (parts.length > 1 && parts[1][0] != " "){
		ns = config['wikipedias'][wikipedia]['namespaces'][parts[0]];
		if (! ns) ns = "wikipedia";
	} else {
		ns = 'article';
	}
	return ns;
}

function dbOpenCheck(err, db){
	console.log("db is open, boss!");
}

db.open(dbOpenCheck);

function saveRecs(msg){
	saveVandals(msg);
}

//mongo business here, to store the data for later use.
function saveVandals(msg){
	

	if (msg.comment.match(/vandal/) && msg.namespace === "article"){
		db.collection('wikiCollection', function(err, collection){
			doc = {
				"time": new Date().getTime(),
				"page": msg.page,
				"url": msg.url,
				//"user": msg.user,
				//"comment": msg.comment
				"delta": msg.delta
			};
			
				collection.insert(doc, function(){
					console.log('Got a record, boss!');
				});	
			   
			});
	}
        
}


exports.listen = listen;