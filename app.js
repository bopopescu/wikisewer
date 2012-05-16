//importing
var fs = require('fs'),
	irc = require('./irc'),
	sys = require('sys'),
	http = require('http'),
	path = require('path'),

	//redis = require('redis'),
	//let us use mongodb
	mongo = require('mongoose'),
	_ = require('underscore'),
	sio = require('socket.io'),
	express = require('express');

//attach configuration

var configPath = path.join(__dirname, "config.json");
var config = JSON.parse(fs.readFileSync(configPath));
var app = module.exports = express.createServer();
var requestCount = 0;
var sockets = [];


//get Wiki shortnames by longnames from config readFileSync
//though since we're only connecting to the engl. channel, probably won't need.
var wikisSorted = [];
for(var channel in config.wikipedias){
	wikisSorted.push(channel);	
} 

wikisSorted.sort(function (a, b){
	w1 = config.wikipedias[a].long;
	w2 = config.wikipedias[b].long;

	if (w1===w2) return 0;
	else if (w1 < w2) return -1;
	else if (w1 > w2) return 1;
});

//the web app

app.configure(function(){
	app.set('views', __dirname + '/views');
	app.set('view engine', 'jade');
	app.use(express.bodyParser());
	app.use(express.methodOverride());
	app.use(app.router);
});

app.configure('development', function(){
	app.use(express.errorHandler({dumpExceptions: true, showStack: true}));
	app.use(express.static(__dirname + '/public'));
});

app.configure('production', function() {
	app.use(express.errorHandler());
	app.use(express.static(__dirname + '/public', {maxAge: 60*15*1000}));
});

app.get('/', function(req, res){
	res.render('index', {
		title: 'wikisewer',
		wikis: config.wikipedias,
		wikisSorted: wikisSorted,
		stream: true,
		trends: false
	});
});

// leaving out the other pages and stats because we just want the barest bones first

app.listen(config.port);

function sendUpdate(message) {
	_.each(sockets, function(socket){
		socket.emit('message', message);

	});
}

var updateStream = irc.listen(config, sendUpdate);
var io = sio.listen(app);

io.configure('production', function() {
	io.enable('browser client etag');
	io.set('log level', 1);
	io.set('transports', [
		'websocket',
		'htmlfile',
		'xhr-polling',
		'jsonp-polling'
	]);
});

io.configure('development', function() {
	io.set('transports', ['websocket']);
});

io.sockets.on('connection', function (socket){
	sockets.push(socket);
	console.log('adding a socket, now. Total = ' + sockets.length);
	socket.on('disconnect', function(){
		sockets = _.without(sockets, socket);
		console.log('removing a socket now. Total = ' + sockets.length);
	});
});