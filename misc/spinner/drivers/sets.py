#
# Sets
#
# Uses Google Sets for spinning new keyword phrases
#

import base, urllib, re
from whois import whois

class Sets(base.Base):
	
	aSet = []

	#
	# Search for a keyword using Google Sets
	#
	def search(self, sPhrase, oCallback):
		self.sPhrase 		= sPhrase
		self.oCallback	= oCallback
		
		self.start()
		
	
		
	#
	# Called when thread is started
	#
	def run(self):
		self.retrieve_set(self.sPhrase)
		
	
	#
	# Retrieve a set from Google Sets
	#
	def retrieve_set(self, sPhrase):
		
		sURL			= self.get_query_url(sPhrase)
		oQuery		= urllib.urlopen(sURL)
		sContent	= oQuery.read()
		aResults	= re.findall('<font.*size=-1><a.*>(.*)<\/a>', sContent)
		
		import unicodedata
		
		for sResult in aResults:
			sResult = sResult.decode("ascii", "ignore")
			oRegex = re.compile('[^a-z]')
			if not oRegex.search(sResult):
				self.aSet.append(sResult)
	
		self.jumble(self.aSet)
		
	
	#
	# Mix-match a group of words
	#
	def jumble(self, aSet):
		aJumble = []
		for x in aSet:
			aJumble.append(x)
			for y in aSet:
				if x != y:
					aJumble.append(x + y)
					aJumble.append(y + x)
					
		self.oCallback('set', aJumble)

		
	
	#
	# Retrieve the query URL for a phrase
	#
	def get_query_url(self, sPhrase, bSmall = True):
		
		if bSmall:
			sSize = 'Shrink'
		else:
			sSize = 'Large'
			
		aParams		= []
		
		def qry_map(x):
			aParams.append(x)
			return 'q%d=%s' % (len(aParams), urllib.quote(x))
			
		sParams	= '&'.join(map(qry_map, sPhrase.split(' ')))
		
 		return 'http://labs.google.com/sets?%s&btn=%s' % (sParams, sSize)

