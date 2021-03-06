# coding=utf-8

# This file contains the SerienRecoder Serien Server stuff

# Constants
SERIES_SERVER_URL = 'http://www.serienserver.de/cache/cache.php'

try:
	import xmlrpclib
except ImportError as ie:
	xmlrpclib = None

class SeriesServer:

	def __init__(self):
		# Check dependencies
		if xmlrpclib is not None:
			self.server = xmlrpclib.ServerProxy(SERIES_SERVER_URL, verbose=False)

	def getSeriesInfo(self, seriesID):
		seriesInfo = self.server.sp.cache.getSeriesInfo(seriesID)
		infoText = ""

		# Fan count
		if 'fancount' in seriesInfo:
			infoText += ("Die Serie hat %s Fans" % seriesInfo['fancount'])

		# Rating
		if 'rating' in seriesInfo:
			infoText += (" und eine Bewertung von %s / 5.0 Sternen" % seriesInfo['rating'])

		# Transmission info
		infoText += "\n\n"
		if 'seasons_and_episodes' in seriesInfo:
			glue = ', '
			infoText += "%s\n" % glue.join(seriesInfo['seasons_and_episodes'])

		if 'transmissioninfo' in seriesInfo:
			infoText += "%s\n" % seriesInfo['transmissioninfo']

		if 'category' in seriesInfo:
			infoText += "%s\n" % seriesInfo['category']

		infoText += "\n"
		# Description
		if 'description' in seriesInfo:
			infoText += seriesInfo['description'].encode('utf-8')

		# Cast / Crew
		if 'cast' in seriesInfo:
			glue = "\n"
			infoText += "\n\nCast und Crew:\n%s\n%s" % (glue.join(seriesInfo['cast']).encode('utf-8'), glue.join(seriesInfo['crew']).encode('utf-8'))
		return infoText

	def doSearch(self, searchString):
		resultList = []
		searchResults = self.server.sp.cache.searchSeries(searchString)
		for searchResult in searchResults['results']:
			resultList.append((searchResult['name'].encode('utf-8'), searchResult['country_year'], str(searchResult['id'])))
		if 'more' in searchResults:
			resultList.append(("... %s%s'%s'" % (searchResults['more'], " weitere Ergebnisse für ", searchString.encode('utf-8')), str(searchResults['more']), "-1"))
		return resultList

	def doGetCoverURL(self, seriesID, seriesName):
		return self.server.sp.cache.getCoverURL(int(seriesID), seriesName)

	def doGetWebChannels(self):
		return self.server.sp.cache.getWebChannels()

