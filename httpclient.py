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
import re

# message for too many args
def help():
	print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
	def __init__(self, code=200, body=""):
		self.code = code
		self.body = body


class HTTPClient(object):
	
	def get_host_port(self,url):

		#default
		host = "localhost"
		port = 80
		path = "/"
		
		if (url[:7]=="http://"):
			host = url[7:]
			url = url[7:]
			
		portRE = re.compile('(.*)\:(\d*)(.*)')
		portMatch = portRE.match(url)
		
		if(not portMatch):
			host = url
		else:
			host = portMatch.group(1)
			port = int(portMatch.group(2))
			path = portMatch.group(3)
		
		print "HOST: "+host
		print "PORT: %d"%port
		
		return host, port, path	

	# connects to a given host and returns a socket descriptor
	def connect(self, host, port):
		
		# store the socket descriptor 
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# get the ip address of a given remote host
		(s, b, ip) = socket.gethostbyname_ex(host)
		remote_ip = ip[0]
		print remote_ip
		# connect to ip on a given port
		sock.connect((remote_ip, port))
		print ("\nSocket connected to "+host+" (IP address: "+remote_ip+") on port %d\n" %port)

		return sock
		

	def get_code(self, data):
		
		# bad request code is default 
		code = 400
		codeRE = re.compile('HTTP/1\.(0|1) (\d*) .*')
		codeMatch = codeRE.match(data)
		
		if(not codeMatch):
			print("Invalid header")
		else:
			code = int(codeMatch.group(2))
		return code

	def get_headers(self,data):
		return None

	def get_body(self, data):
		return None

	# read everything from the socket
	def recvall(self,sock):
		data = sock.recv(1024)
		print(data)
		return data
		
		'''
		buffer = bytearray()
		done = False
		
		while not done:
			part = sock.recv(1024)
			if (part):
				buffer.extend(part)
			else:
				done = not part
				
		return str(buffer)
		'''
		
	def GET(self, url, args=None):
		
		(host, port, path) = self.get_host_port(url)
		
		print("\nTry sending GET "+path+" to "+host+" on port %d"%port)
		
		# start a connection with the given host
		sock = self.connect(host, port)
		
		# send message to host
		message = ("GET "+path+" HTTP/1.1\r\nHost: "+host+":%d\r\n\r\n"%port)
		print("Message sent: \n"+ message+"\n\n")
		sock.sendall(message)
		data = self.recvall(sock)
		code = self.get_code(data)
		body = data
		
		# close the connection
		sock.close
		print("\nSocket closed")
		
		return HTTPRequest(code, body)

	# TODO fix this
	def POST(self, url, args=None):
		return self.GET(url)
		'''
		code = 500
		body = "post test"
		return HTTPRequest(code, body)
		'''

	# send to GET or POST function, depending on command
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
		
		request_type = sys.argv[1]
		url = sys.argv[2]
		
		http_request = client.command(url, request_type)
		print("\nHTTPRequest code: %d" %http_request.code)
		print("\nHTTPRequest body: " + http_request.body + "\n")
		
	
	# TODO fix this
	# more than 2 args given
	else:
		help()
		sys.exit(1)
		#print client.command( command, sys.argv[1] )
		#print (command, sys.argv[1])	
	
	
	
