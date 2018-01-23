# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    thread.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kcheung <kcheung@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/01/11 16:54:54 by kcheung           #+#    #+#              #
#    Updated: 2018/01/22 19:00:18 by kcheung          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/python3

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

def get_coin(page):
	container = page.findAll("div", {"class" : "row bottom-margin-1x"})
	container = container[0]
	coin = container.findAll("small", {"class" : "bold hidden-xs"})[0].text
	coin = coin.strip('()')
	return(coin)

def get_price(page):
	container = page.findAll("div", {"class" : "row bottom-margin-1x"})
	container = container[0]
	price = container.findAll("span", {"id" : "quote_price"})[0]["data-usd"]
	return(price)

def get_img(page):
	container = page.findAll("div", {"class" : "row bottom-margin-1x"})
	container = container[0]
	img = container.findAll("img")[0]["src"]
	return(img)

def get_tool(page):
	container = page.findAll("div", {"id" : "tools"})
	container = container[0]
	tool_script = container.findAll("textarea", {"class" : "form-control"})[0].text
	return(tool_script)

def worker(q, fd, entry):
	# print(threading.currentThread().getName(), 'starting')
	logging.debug('starting')
	while not q.empty():
		url = q.get()
		r = urlopen(url)
		if r.getcode() == 200:
			page_html = urlopen(url).read()
			page_soup = soup(page_html, "html.parser")
			coin = get_coin(page_soup)
			price = get_price(page_soup)
			img = get_img(page_soup)
			tool_script = get_tool(page_soup)
			print(coin  + " : " + price + " : " + img + " : " + tool_script)
			fd.write(coin + ',' + price + '\n')
			q.task_done()
		else:
			logging.debug('request error')
	# print(threading.currentThread().getName(), 'Exiting')
	logging.debug('exiting')

def get_cryptoList():
	r = urlopen('https://coinmarketcap.com/all/views/all/')
	print(r.getcode())
	if r.getcode() == 200:
		index_html = r.read()
		index_soup = soup(index_html, "html.parser")
		containers = index_soup.findAll("a", {"class" : "currency-name-container"})
		links = []
		for container in containers:
			links.append(container['href'])

# Put links into Queue for processing
	q = Queue()
	base = 'https://coinmarketcap.com'
	links = list(map(lambda x: base+x, links))
	for l in links:
		q.put(l)
	return (q)


def main():
	filename = "coins.csv"
	fd = open(filename, "a+")
	headers = "Coin, USD\n"
	fd.write(headers)

	startTime = datetime.now()
	q = get_cryptoList()

	entry = {}
	for i in range(10):
		t = threading.Thread(name='worker:'+ str(i), target=worker,args=(q, fd, entry))
		t.start()
	q.join()
	fd.close()
	print (datetime.now() - startTime)

if __name__ == '__main__':
	main()
