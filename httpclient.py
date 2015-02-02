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

# message for no args
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
		# optional TODO: there must be a better way to do this...
		if (url[:8]=="https://"):
			url = url[8:]
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
		# print "HOST: "+host
		# print "PORT: %d"%port
		# print "PATH: "+path
		
		return host, port, path	


	# connects to a given host on a given port and returns a socket descriptor
	def connect(self, host, port):
		
		# store the socket descriptor 
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# get the ip address of a given host
		# alternative code:
		# (hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex(host)
		# remote_ip = ipaddrlist[0]
		ip = socket.gethostbyname(host)
		
		# connect to ip on a given port
		sock.connect((ip, port))
		
		# TESTING
		# print ("\nSocket connected to "+host)
		# print (" (IP address: "+ip+") on port %d\n" %port)
		
		# return socket descriptor
		return sock
		
	
	# returns the http status code given a string containing the server response
	def get_code(self, data):
		
		# internal server error is default status code 
		code = 500
		
		# extract the status code from the header
		codeRE = re.compile('HTTP/1\.(0|1) (\d*) .*')
		codeMatch = codeRE.match(data)
		
		if(codeMatch):
			code = int(codeMatch.group(2))
			
		return code


	# returns the content before \r\n\r\n
	def get_headers(self,data):
		
		headerRE = re.compile('(.*?)(\r\n\r\n.*)', flags = re.DOTALL)
		headerMatch = headerRE.match(data)
		
		if(headerMatch):
			data = headerMatch.group(1)
		
		return data

	
	# returns the content after \r\n\r\n
	def get_body(self, data):
		
		bodyRE = re.compile('(.*?)(\r\n\r\n.*)', flags = re.DOTALL)
		bodyMatch = bodyRE.match(data)
		
		if(bodyMatch):
			data = bodyMatch.group(2)
			
		return data


	# reads and returns everything from the socket
	def recvall(self,sock):
	
		buffer = bytearray()
		done = False
		
		while not done:
			part = sock.recv(1024)
			if (part):
				buffer.extend(part)
			else:
				done = not part

		return str(buffer)
		
	
	# connects to socket, sends message, recieves data, and closes connection
	def send_message(self, host, port, message):
		
		# start a connection with the given host
		sock = self.connect(host, port)
		
		# TESTING
		# print("Message sent: \n"+ message+"\n\n")
		
		# send message to host
		sock.sendall(message)
		
		# receive data from the host
		data = self.recvall(sock)
		
		# close the connection
		sock.close()
		
		# TESTING
		# print("\nSocket closed")
		
		return data
	
	
	# send GET request to server	
	def GET(self, url, args=None):
		
		(host, port, path) = self.get_host_port(url)
		
		# TESTING
		# print("\nTry sending GET "+path+" to "+host+" on port %d"%port)
		
		# TODO: find out if connection: close is correct
		message = ("GET "+path+" HTTP/1.1\r\nHost: "+host+":%d\r\nConnection: close\r\n\r\n"%port)
		
		data = self.send_message(host, port, message)
		
		# retrieve the status code and body of the response
		code = self.get_code(data)
		body = self.get_body(data)
		
		return HTTPRequest(code, body)


	# send POST request to server
	def POST(self, url, args=None):
		
		(host, port, path) = self.get_host_port(url)
		
		# TESTING
		# print("\nTry sending POST "+path+" to "+host+" on port %d"%port)
		
		# default 
		message = ("POST "+path+" HTTP/1.1\r\nHost: "+host+":%d\r\n"%port)
		
		# if no args are specified - should never happen
		if (not args):
			message = message + "Connection: close\r\n\r\n"
		
		# when args are specified
		else:
			params = urllib.urlencode(args)
			
			# get the length of the content to send
			contentlength = len(str(params))
		
			message = message + ("Content-Length: %d\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n"%contentlength)
			message = message + params
			
		data = self.send_message(host, port, message)
		
		code = self.get_code(data)
		body = self.get_body(data)
		
		return HTTPRequest(code, body)
		
		
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
	
	# 1 arg given
	else:
		url = sys.argv[1]
		http_request = client.command(url, command)
		
	# TESTING
	print("\nHTTPRequest code: %d" %http_request.code)
	print("\nHTTPRequest body: " + http_request.body + "\n")
	
	
	
