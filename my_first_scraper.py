#!/bin/python3

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=video%20card'
my_url = 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html, "html.parser")
# print(page_soup.h1)
# print(page_soup.p)

# grab each product
containers = page_soup.findAll("div", {"class" : "item-container"})
# print(len(containers))
# container = containers[0]
# print(containers[0].div.div.a.img['title'])

filename = "products.csv"
f = open(filename, "w")
headers = "brand, product_name, shipping\n"
f.write(headers)

#for each product get brand,title,shipping
for container in containers:
	brand = container.div.div.a.img['title']
	title = container.findAll("a", {"class" : "item-title"})[0].text
	shipping = container.findAll("li", {"class" : "price-ship"})[0].text.strip()
	f.write(brand.replace(",", "|") + "," + title.replace(",", "|") + "," + shipping + "\n")
f.close()

