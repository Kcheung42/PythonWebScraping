# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    crawler.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kcheung <kcheung@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/01/17 13:24:33 by kcheung           #+#    #+#              #
#    Updated: 2018/01/17 14:39:05 by kcheung          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from bs4 import BeautifulSoup
from urllib.request import urlopen
from queue import Queue
import threading
import loggin
import re

host = 'https://www.google.com/search?source=hp&ei=9MhfWpXhKMbSjAPC3pDABQ&q=jobs&oq=jobs&gs_l=psy-ab.3..0i67k1j0i131i67k1j0i131i20i263k1j0i131i20i263i264k1j0i131i67k1j0i131k1j0l4.4098.7740.0.7865.8.5.2.0.0.0.75.272.4.5.0....0...1c.1.64.psy-ab..1.7.332.6..35i39k1.56.QidD5pWyJPE'

# logging.basicConfig(filename='debug.log', level=logging.DEBUG,
# 		format='[%(levelname)s] (%(threadName) - 10s) %(message)s'
# )

def worker(q):
	# logging.debug('starting')
	while not q.empty():
		url = q.get()
		scrape(url, q)
		q.task_done()
	# logging.debug('ending')

def main():
	q = Queue()
	q.put(host)
