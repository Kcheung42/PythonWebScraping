# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    cryptothread2.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kcheung <kcheung@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/01/11 16:54:54 by kcheung           #+#    #+#              #
#    Updated: 2018/01/11 18:47:21 by kcheung          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

'''
This Script will Scrape coinmarketcaps website for all Coins and USD price.
Data will be saved in a CSV formated file

This example implements a Queue and Debug Logging
'''
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from queue import Queue
import threading
import os
import logging

#1 debug =detailed info
#2 info =detailed info
#3 warning =detailed info
#4 error =detailed info
#5 critical =detailed info

logging.basicConfig(filename='WebScraperlogfile.log',level=logging.DEBUG,
					format='[%(levelname)s] (%(threadName) - 10s) %(message)s',
					)

filename = "coins.csv"
f = open(filename, "a+")
headers = "Coin, USD\n"
f.write(headers)

index_html = urlopen('https://coinmarketcap.com/all/views/all/').read()
index_soup = soup(index_html, "html.parser")
containers = index_soup.findAll("a", {"class" : "currency-name-container"})
links = []
for container in containers:
	links.append(container['href'])

links = []
# Put links into Queue for processing
q = Queue()
base = 'https://coinmarketcap.com'
links = list(map(lambda x: base+x, links))
for l in links:
	q.put(l)

startTime = datetime.now()
def worker(q):
	# print(threading.currentThread().getName(), 'starting')
	logging.debug('starting')
	while not q.empty():
		url = q.get()
		page_html = urlopen(url).read()
		page_soup = soup(page_html, "html.parser")
		container = page_soup.findAll("div", {"class" : "row bottom-margin-1x"})
		coin = container[0].findAll("small", {"class" : "bold hidden-xs"})[0].text
		price = container[0].findAll("span", {"id" : "quote_price"})[0]["data-usd"]
		print(coin  + ":" + price)
		f.write(coin + ',' + price + '\n')
		q.task_done()
	# print(threading.currentThread().getName(), 'Exiting')
	logging.debug('exiting')

for i in range(10):
	t = threading.Thread(name='worker:'+ str(i), target=worker,args=(q,))
	t.start()
q.join()
f.close()
print (datetime.now() - startTime)
