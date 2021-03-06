﻿# -*- coding: utf-8 -*-
from __init__ import _

import re

from twisted.web.client import getPage
from twisted.internet import defer

import socket
from urllib import urlencode
from urllib2 import urlopen, Request, URLError

from Components.config import config

from SerienRecorderHelpers import *

class WebChannels(object):
	def __init__(self, user_callback=None, user_errback=None):
		self.user_callback = user_callback
		self.user_errback  = user_errback

	def	request(self):
		print "[SerienRecorder] request webpage.."
		url = "http://www.wunschliste.de/updates/stationen"
		getPage(getURLWithProxy(url), agent=getUserAgent(), headers=getHeaders()).addCallback(self.__callback).addErrback(self.__errback, url)

	def request_and_return(self):
		print "[SerienRecorder] request_and_return webpage.."
		url = "http://www.wunschliste.de/updates/stationen"
		req = Request(getURLWithProxy(url), headers=getHeaders())
		try:
			data = urlopen(req).read()
		except URLError as e:
			self.__errback(str(e), url)
		except socket.timeout as e:
			self.__errback(str(e), url)
		return self.__callback(data)

	def __errback(self, error, url=None):
		print error
		if (self.user_errback):
			self.user_errback(error, url)

	def __callback(self, data):
		data = processDownloadedData(data)
		stations = re.findall('<option value=".*?>(.*?)</option>', data, re.S)
		if stations:
			web_chlist = []
			for station in stations:
				if station != 'alle':
					station = doReplaces(station)
					web_chlist.append((station.replace(' (Pay-TV)','').replace(' (Schweiz)','').replace(' (GB)','').replace(' (&Ouml;sterreich)','').replace(' (USA)','').replace(' (RP)','').replace(' (F)','').replace('&#x1f512;','')))

		if (self.user_callback):
			self.user_callback(web_chlist)

		return web_chlist
