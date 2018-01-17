# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logExample.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kcheung <kcheung@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/01/11 18:10:04 by kcheung           #+#    #+#              #
#    Updated: 2018/01/11 18:25:27 by kcheung          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging

logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
# logging.basicConfig(filename='logfile.log', level=logging.CRITICAL)

def main():
	try:
		logging.debug("We're here in the main try loop")
		# mathFail = 1/0
		if 1<2:
			logging.debug('entered into the first statement')
			print('Hello')
			try:
				urllib2.urlopen('http://google.com').read()
			except Exception as e:
				logging.error('urllib url visited failed, for the reason of %s' % str(e))
		else:
			logging.debug('entered into the first statement')
			print('YO')
	except Exception as e:
		logging.critical(str(e))

main()
