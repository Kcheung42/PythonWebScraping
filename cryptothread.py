# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    cryptothread.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kcheung <kcheung@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/01/11 18:10:01 by kcheung           #+#    #+#              #
#    Updated: 2018/01/16 17:22:52 by kcheung          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

'''
This Script will Scrape coinmarketcaps website for all Coins and USD price.
Data will be saved in a CSV formated file
'''
from datetime import datetime
from threading import Thread
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename = "coins.csv"
f = open(filename, "a+")
headers = "Coin, USD\n"
f.write(headers)

index_html = uReq('https://coinmarketcap.com/all/views/all/').read()
index_soup = soup(index_html, "html.parser")
containers = index_soup.findAll("a", {"class" : "currency-name-container"})
links = []
for container in containers:  ## store all links in links[] array
	links.append(container['href'])


startTime = datetime.now()
def th(cur):
	base = 'https://coinmarketcap.com'
	url = base + cur
	page_html = uReq(url).read()
	page_soup = soup(page_html, "html.parser")
	container = page_soup.findAll("div", {"class" : "row bottom-margin-1x"})
	coin = container[0].findAll("small", {"class" : "bold hidden-xs"})[0].text
	price = container[0].findAll("span", {"id" : "quote_price"})[0]["data-usd"]
	print(coin  + ":" + price)
	f.write(coin + ',' + price + '\n')

threadlist = []
print(links)

for u in links:
	t = Thread(target=th,args=(u,))
	t.start()
	threadlist.append(t)

for b in threadlist:
	b.join()

f.close()

print (datetime.now() - startTime)
