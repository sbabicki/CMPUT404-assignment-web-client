#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#	 http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

# message for too many args
def help():
	print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
	def __init__(self, code=200, body=""):
		self.code = code
		self.body = body


class HTTPClient(object):
	#def get_host_port(self,url):

	# connects to a given host and returns a socket descriptor
	def connect(self, host, port):
		
		# self.socket is the socket descriptor 
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# get the ip address of a given remote host
		remote_ip = socket.gethostbyname(host)
	
		# connect to ip on a given port
		self.socket.connect((remote_ip, port))
		print ("\nSocket connected to "+host+" (IP address: "+remote_ip+") on port %d\n" %port)
		
		return self.socket
		

	def get_code(self, data):
		return None

	def get_headers(self,data):
		return None

	def get_body(self, data):
		return None

	# read everything from the socket
	def recvall(self):
		buffer = bytearray()
		done = False
		while not done:
			part = self.socket.recv(1024)
			if (part):
				buffer.extend(part)
			else:
				done = not part
		return str(buffer)

	def GET(self, url, args=None):
		code = 500
		body = ""
		return HTTPRequest(code, body)

	def POST(self, url, args=None):
		code = 500
		body = ""
		return HTTPRequest(code, body)

	def command(self, url, command="GET", args=None):
		if (command == "POST"):
			return self.POST( url, args )
		else:
			return self.GET( url, args )

	
if __name__ == "__main__":
	client = HTTPClient()
	command = "GET"
	
	if (len(sys.argv) <= 1):
		help()
		sys.exit(1)
		
	# 2 args given
	elif (len(sys.argv) == 3):
		print client.command( sys.argv[1], sys.argv[2] )

		request_type = sys.argv[1]
		host = sys.argv[2]
		
		print("Try sending "+request_type+" to "+host)
		# start a connection with the given host
		sock = client.connect(host, 80)
		
	
	# TODO fix this
	# more than 2 args given
	else:
		print client.command( command, sys.argv[1] )
		print (command, sys.argv[1])	
	
	# close the connection
	sock.close
	
