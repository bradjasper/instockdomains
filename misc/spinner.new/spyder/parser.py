from HTMLParser import HTMLParser
#import sgmllib
import re

#
# Spyder_Parser
#
# Spyder HTML Parser
#
class Spyder_Parser(HTMLParser):
	
	sURL		= ''
	aURLs	 	= []
	sData		=	''
	aWords	= []
		
	#
	# Set the URL to use as a base
	#
	def set_url(self, sURL):
		self.sURL = sURL
	
	#
	# Retrieve the list of URLs
	#	
	def get_urls(self):
		return self.aURLs
	
	#
	# Retreive array of unique words
	#
	def get_words(self):
		return self.aWords
		
	
	#
	# Initialize!
	#
	def __init__(self, bUnique = True):
		HTMLParser.__init__(self)
#		sgmllib.SGMLParser.__init__(self, 0)
		
		self.bUnique = bUnique
		
	
	#
	# Handle raw data
	#
	def handle_data(self, sData):
		aIgnore			= ['help', 'www', 'srp', 'sup', 'searchscan', 'mcafee', 'function', 'all', 'video', 'beta', 'news', 'search', 'com', 'yahoo', 'http', 'and', 'yfp', 'sado', 'utf', 'the', 'span', 'yimg', 'for', 'cached', 'web']
		sData				= re.sub("[^a-zA-Z]", " ", sData)
		aWords			= sData.split(' ')
		
		for sWord in aWords:
			if len(sWord) > 2:
				
				sWord = sWord.lower()
			
				if sWord in aIgnore:
					continue
					
				if self.bUnique:
					if self.array_value_exists(sWord, self.aWords) == True:
						continue
						
				self.aWords.append(sWord)

	
	#
	# Called after feed() is called. Used to strip out URLs
	#	
	def handle_starttag(self, sTag, kAttrs):
	
		try:
			if sTag == "a":
				for key, value in kAttrs:
					if key == "href":
						sURL = re.sub("%20", " ", value)

						#	Strip out invalid links
						if re.match("^(?!javascript*)", sURL):

							# Check for relative URL's
							if re.match("^(?!http:\/\/*)", sURL):

								sURL	= self.sURL + sURL
						
							if self.array_value_exists(sURL, self.aURLs) == False:
								self.aURLs.append(sURL)
		except Exception, e:
			print e

							
	#
	# Check if a value is already listed in an array
	#
	def array_value_exists(self, sNeedle, aHaystack):
		for sHaystack in aHaystack:
			if sHaystack == sNeedle:
				return True

		return False
		
	
	#
	# Tidy HTML
	#
	def tidy(self, sContents):
		import os
		print os.popen("echo '" + sContents + "' | tidy -q").read()
		