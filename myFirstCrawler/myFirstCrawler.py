# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    myFirstCrawler.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kcheung <kcheung@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/01/11 18:27:17 by kcheung           #+#    #+#              #
#    Updated: 2018/01/11 20:57:32 by kcheung          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from bs4 import BeautifulSoup
from urllib.request import urlopen
from queue import Queue
import threading
import logging
import re

logging.basicConfig(filename='debug.log',level=logging.DEBUG,
					format='[%(levelname)s] (%(threadName) - 10s) %(message)s',
					)
visited = set()
q = Queue()
filename = 'All_links.txt'
f = open(filename, 'a+')
headers = "tittle, link_address\n"
f.write(headers)
host = 'http://books.toscrape.com/'

def scrapeForLinks(url, q):
	try:
		content = urlopen(url).read()
		soup = BeautifulSoup(content, "html.parser")
		for link in soup.findAll('a'):
			try:
				href = link['href']
				try:
					title = link.text.strip()
				except Exception as e:
					logging.debug("no text")
					try:
						title = link['title']
					except Exception as e:
						logging.debug("no title attrib")
				if not href.startswith('/..'):
					href = host + href
					if href not in visited:
						visited.add(href)
						q.put(href)
						f.write(title + ',' + href + '\n')
						print(link.text.strip())
			except KeyError:
				logging.debug("KeyError")
	except Exception as e:
		logging.debug(str(e))

def worker(q):
	logging.debug('starting')
	while not q.empty():
		url = q.get()
		scrapeForLinks(url,q)
		q.task_done()
	logging.debug('ending')

def main():
	q.put(host)
	worker(q)
	for i in range(5):
		t = threading.Thread(name='worker'+str(i), target=worker, args=(q, ))
		t.start()
	q.join()
	f.close()

main()
