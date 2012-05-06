$(document).ready(init);

var pause = false;
var deltaLimit = 0;
var wikipediaLimit = "all";
var namespaceLimit = "all";
var includeRobots = true;
var includeUsers = true;
var includeAnonymous = true;

function init(){
	setupControls();
	var socket = io.connect();
	socket.on('message', function(msg){
		if (pause) return;
		if (!wikipediaFilter(msg)) return;
		if (!userFilter(msg)) return;
		if (!namespaceFilter(msg)) return;
		if (Math.abs(msg.delta) < deltaLimit) retunr;

		addUpdate(msg);
		removeOld();

	});
}

function addUpdate(msg){
	var lang = $('<span>').attr({'class': 'lang'}).text('[' + msg.wikipediaLong + ']');
	var a = $('<a>').attr({'class': 'page', 'href': msg.url, 'title': msg.comment, target: '_new'}).text(msg.page);
	var comment = $('<span>').attr({'class': 'comment'}).text(msg.comment);
	var delta;
	if (msg.delta == null) delta = "n/a";
	else if (msg.delta < 0) delta = msg.delta;
	else delta = "+" + msg.delta;
	delta = $('<span>').attr({'class': 'delta'}).text(delta);

	updateClasses = ['update'];

	if (msg.newPage) updateClasses.push('newPage');
	if (msg.unpatrolled) updateClasses.push('unpatrolled');

	var d = $('<div>').attr({'class': updateClasses.join(' ')})
		.append(lang)
		.append(a)
		.append(delta)
		.append(comment)
		.hide();
	$('#updates').prepend(d);
	d.slideDown('slow');

	//here went the background code, augment to create view of diffs
}

function removeOld(){
	var old = $('.update').slice(50)
	old.fadeOut('fast', function() { old.detach(); });	
}

function togglePause(){
	pause = !pause;
	if (pause) {
		$('header').block({
			message: '<br/Paused<br/> Press \'p\' to resume',
			css: {
				'border': 'none',
				'color': 'black',
				'opacity': '1',
				'width': '280px',
				'height': '70px'

			}
		});
	
	} else {
		$('header').unblock();
	}
}

function setupControls(){
	$('#slider').slider({
		range: 'min',
		value: 0,
		min: 0,
		max: 1000,
		step: 50,
		slide: function(event, ui){
			deltaLimit = parseInt(ui.value);
			$('#deltaLimit').text(ui.value);
		}
	});

	$(document).bind('keyup', 'p', togglePause);
	$(document).bind('keyup', 'pause', togglePause);

}



function wikipediaFilter(msg) {
  if (wikipediaLimit == "all") return true;
  if (wikipediaLimit == msg.wikipedia) return true;
  return false;
}

function namespaceFilter(msg) {
  if (namespaceLimit == "all") return true;
  if (namespaceLimit == msg.namespace) return true;
  return false;
}

function userFilter(msg) {
  if (! includeRobots && msg.robot) {
    return false;
  } else if (! includeAnonymous && msg.anonymous) {
    return false;
  } else if (! includeUsers && (! msg.anonymous && ! msg.robot)) {
    return false;
  }
  return true;
}
