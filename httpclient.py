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
	
	# returns the host, port, and path from a given url
	def get_host_port(self,url):

		#default
		host = "localhost"
		port = 80
		path = "/"
		
		# remove the "http://" begining if it exists
		if (url[:7]=="http://"):
			url = url[7:]
			host = url
		
		# separate the host port and path	
		portRE = re.compile('(.*)\:(\d*)(.*)')
		portMatch = portRE.match(url)
		
		# if no port, separate the host and path (separated by "/")
		if(not portMatch):
			pathRE = re.compile('(.*?)(/.*)')
			pathMatch = pathRE.match(url)
			
			# no path specified
			if(not pathMatch):
				host = url
			
			# extract the host and path
			else:
				host = pathMatch.group(1)
				path = pathMatch.group(2)
		
		# host, port, and path are specified
		else:
			host = portMatch.group(1)
			port = int(portMatch.group(2))
			path = portMatch.group(3)
		
		# TESTING
		print "HOST: "+host
		print "PORT: %d"%port
		print "PATH: "+path
		
		return host, port, path	


	# connects to a given host on a given port and returns a socket descriptor
	def connect(self, host, port):
		
		# store the socket descriptor 
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# get the ip address of a given host
		# alternative code:
		#(hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex(host)
		#remote_ip = ipaddrlist[0]
		ip = socket.gethostbyname(host)
		
		# connect to ip on a given port
		sock.connect((ip, port))
		print ("\nSocket connected to "+host+" (IP address: "+ip+") on port %d\n" %port)
		
		# return socket descriptor
		return sock
		
	
	# returns the http status code given a string containing the server response
	def get_code(self, data):
		
		# internal server error is default status code 
		code = 500
		
		# extract the status code from the header
		codeRE = re.compile('HTTP/1\.(0|1) (\d*) .*')
		codeMatch = codeRE.match(data)
		
		if(not codeMatch):
			print("Response uses invalid syntax")
		else:
			code = int(codeMatch.group(2))
		return code


	def get_headers(self,data):
		return None


	def get_body(self, data):
		return None


	# TODO: get buffer to work
	# read everything from the socket
	def recvall(self,sock):
		
		data = sock.recv(1024)
		
		# print server response to stdout
		print(data)
		return data
		
		'''
		buffer = bytearray()
		done = False
		while not done:
			print("START LOOP")
			part = sock.recv(1024)
			print("recieved")
			if (part):
				print("PART: "+part)
				buffer.extend(part)
				print("next")
			else:
				done = not part
				print("done = not part")
		print("END LOOP")
		return str(buffer)
		'''
	
	# send GET request to server	
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

	# TODO: send GET request to server
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
		
		# TESTING
		print("\nHTTPRequest code: %d" %http_request.code)
		print("\nHTTPRequest body: " + http_request.body + "\n")
		
	
	# TODO: send args
	# more than 2 args given
	else:
		help()
		sys.exit(1)
		#print client.command( command, sys.argv[1] )
		#print (command, sys.argv[1])	
	
	
	
