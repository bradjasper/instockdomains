#
#	BOSS
#
#	Uses Yahoo's BOSS API to query for 
# the number of results a given keyword has
# and any related keywords
#

import urllib, threading, simplejson, re
from wordle import wordle

API_URL				= 'http://boss.yahooapis.com/ysearch/%s/v1/%s?appid=%s'
API_KEY				= '###'
QUERY_TERMS		= ['nancy', 'the', 'boombay', 'rocking', 'dude', 'where', 'is', 'my', 'car', 'bob', 'mac', 'tips', 'mactips']
QUERY_RESULTS	= {}
THREADS				= {}

class BOSS(threading.Thread):
	

	#
	# Called when BOSS is initialized
	#
	def __init__(self, sQuery, oCallback):
		threading.Thread.__init__(self)

		self.sQuery			= sQuery
		self.oCallback	= oCallback
		self.start()
		
	#
	#	var_dump for python
	#
	def info(self, v):
		return '%s = %r %s' % (v, v, type(v))
		
	#
	# Called when thread is first started
	#
	def run(self):
		self.query(self.sQuery)

		
	
	#
	# Send a query to the BOSS API Server
	#
	def query(self, sQuery):
		
		sURL									= self.get_api_url(sQuery)
		oQuery								= urllib.urlopen(sURL)
		self.sContents				= oQuery.read()	
		self.oResults					= simplejson.loads(self.sContents)		
		self.close()
		oWordle	= wordle.Wordle()
		
		for oResult in self.get_results():

			try:
				oWordle.feed(oResult['title'])
				oWordle.feed(oResult['abstract'])
			except UnicodeEncodeError, e:
				pass

		print oWordle.get_unique()
	
	#
	# Return the results
	#
	def get_results(self):
		return self.oResults['ysearchresponse']['resultset_' + self.sType]
	
	#
	# Return the api url for a specific query
	#
	def get_api_url(self, sQuery, sType = 'web'):
		self.sType = sType
		return API_URL % (sType, urllib.quote(sQuery), API_KEY)
		
	
	
	#
	# Called when a thread is closed
	#
	def close(self):
		if threading.activeCount() == 2:
			
			#	Insert threads into database
			self.oCallback('boss_results', 'boom')

	
	#
	# Return a property from the results
	#
	def property(self, sProp):
		return self.oResults['ysearchresponse'][sProp]

#while len(QUERY_TERMS):
#	nIndex					= len(THREADS)
#	THREADS[nIndex] = BOSS()
	