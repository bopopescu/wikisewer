#!/usr/bin/env python

import re
import json
import time

from requests import post, get

def wikipedia_updates(callback):
	endpoint = "http://localhost:3000/socket.io/1"
	session_id = post(endpoint).content.split(':')[0]
	xhr_endpoint = "/".join((endpoint, "xhr-polling", session_id))

	while True:
		t = time.time() * 1000000
		response = get(xhr_endpoint, params={'t': t}).content.decode('utf-8')
		
		chunks = re.split(u'\ufffd[0-9]+\ufffd', response)
		for chunk in chunks:
			parts = chunk.split(':', 3)
			if len(parts) == 4:
				callback(json.loads(parts[3]))
if __name__ == "__main__":
	def print_page(update):
		print update
	
	wikipedia_updates(print_page)
