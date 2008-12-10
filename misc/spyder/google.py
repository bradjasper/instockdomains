#
# Google
#
# Interface for dealing with Google services
#
# Ex. Google Sets
#

import urllib, re, threading

class Google(threading.Thread):
	
	#
	# Constructor
	#
	def __init__(self, aQueries, oCallback = {}):

		self.aQueries		= aQueries
		self.oCallback	= oCallback
		
		threading.Thread.__init__(self)
		
		self.start()
		
	#
	# Called when thread is started
	#
	def run(self):

		self.aSet		= self.get_set(self.aQueries)
		
		sKey = ' '.join(self.aQueries)

		self.aFinal	= {sKey: self.aSet}
		
		if callable(self.oCallback):
			self.oCallback('google', 'set_data', self.aFinal)
			
			if threading.activeCount() == 2:
				self.oCallback('google', 'set_finished', '')
					
	#
	# Query Google Sets for synonyms
	#
	def get_set(self, aQueries):
		
		oSet			= urllib.urlopen(self.get_query_url(aQueries))
		sContent	= oSet.read()
		aResults	= re.findall('<font(.*)size=-1><a(.*)>(.*)<\/a>', sContent)
		aSet			= {}
		
		for aResult in aResults:
			sWord = re.sub('[^a-zA-Z ]', '', aResult[2]).lower()
			if len(sWord):
				nLen				= len(aSet)
				aSet[nLen]	= sWord
				
		return aSet
		
	
	#
	# Fire an event
	#
	def fire_event(self, sEvent, oCallback = {}):
		
		if callable(oCallback):
			print threading.activeCount()
	
		
	#
	# Return the URL for a specific query
	#
	def get_query_url(self, aQueries, sSize = 'Shrink'):
		
		sURL			= 'http://labs.google.com/sets?%s&btn=%s'
		sQueries	= ''
		
		# Setup query string arguments
		for i in range(0, len(aQueries)):
			if sQueries != '':
				sQueries += '&'
				
			sQueries += "q%d=%s" % (i+1, urllib.quote(aQueries[i]))

		return sURL % (sQueries, sSize) 

	