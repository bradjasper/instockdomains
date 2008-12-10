#
# Wordle
#
# Wordle does fun things with words
#
# Like sorting, matching, filtering, etc...
#
# This may become a C program some day
#
# The interface should remain the same
#
#
import re

NONE		= 0
LEFT 		= 1
RIGHT 	= 2
CENTER 	= 4

class Wordle(object):
	
	aWords			= []
	sFeed				= ''
	aFeed				= []
		
	#
	# Feed a line into Wordle, stripping out
	# unwanted and duplicate words
	#
	def feed(self, sLine):
		self.sFeed += ' ' + sLine.decode('iso-8859-1')
		
	
	#
	# Feed an array of words
	#
	def feed_array(self, sStr, bClean = False):
		
		if bClean: sStr = self.clean(sStsr)
			
		self.aFeed.append(sStr)
		
		
	
	#
	# Return a unique list of words from the feed
	#
	def get_unique(self):
		
		sClean	= self.clean(self.sFeed)
		aList		= sClean.split(' ')
		aWords	= {}
		
		for sWord in aList:
			if aWords.has_key(sWord):
				aWords[sWord] += 1
			else:
				aWords[sWord]	= 0
		
	
	#
	# Clean a feed of nasty characters
	#
	#	TODO:	Compile into one regular expression
	#
	def clean(self, sFeed):
		sClean	= re.sub(r'<.*?>', '', sFeed)
		sClean	= re.sub('[^a-zA-Z]', ' ', sClean)
		sClean	= re.sub('\W+', ' ', sClean)
		
		return sClean.lower()
	
	
	
	#
	# Return an array frequency
	#
	def frequency(self, sWords):
	
		aWords	= sWords.split(' ')
		
		# Get array value frequency
		aFreq		= [(i, aWords.count(i)) for i in set(aWords)]

		#	Sort by frequency
		aFreq.sort(lambda x,y: cmp(y[1],x[1]))
		
		return aFreq
		
	#
	# Combine two dictionaries adding their common properties
	#
	def combine(self, kDictOne, kDictTwo):

		for sKey, nValue in kDictOne.iteritems():
			if sKey in kDictTwo.keys():
				kDictTwo[sKey] += nValue
			else:
				kDictTwo[sKey] = nValue

		return kDictTwo		
		
	#
	# Array Ninja does magic
	#
	def array_ninja(self, aSets, nLimit = 10):

		aKeys			= aSets.keys()		
		sContent	= ''

		#	Join words into string
		for sKey in aKeys:
			if len(sContent):
				sContent += ' '
				
			sContent	+= ' '.join(aSets[sKey].itervalues())
			
		aFreq	= self.frequency(sContent)
		
		for sSet, aSet in aSets.iteritems():
			for sWord, nFreq in aFreq[:10]:
				if sWord in aSet.values():
					print sSet, sWord
