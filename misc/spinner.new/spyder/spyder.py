import urllib, re, threading
from Queue import Queue
import parser

#
# Spyder
#
#	A web cralwer in its most basic form.
#	Spyder hooks into other modules and performs
# tasks like collecting links and finding unique words
#
class Spyder(threading.Thread):
	
	sRaw			= ''
	sContent	= ''
	sURL			= ''
	aWords		= []
	aURLs			= []
	nDepth		= 1
	
	#
	# Called when thread is started
	#	
	def run(self):
		self.read(self.sURL)
	
	#
	#	Set the URL to spider
	#
	def set_url(self, sURL):
		self.sURL = sURL
			
	#
	# Read contents from a webpage
	#	
	def read(self, sURL, bUnique = True):
		
		hFile						= urllib.urlopen(sURL)
		self.sRaw				= hFile.read()
		hFile.close()
		
		self.parse(self.sRaw, bUnique)
		
		return self.aWords
		
	#
	# Parse the contents of a web page
	#
	# 	- This removes all HTML/Tags
	#		- Grabs unique words
	#		- Returns an array
	#
	def parse(self, sContents, bUnique = True):
		
		hParser = parser.Spyder_Parser(bUnique)
		hParser.set_url(self.sURL)
		sContents	 = hParser.tidy(sContents)
		hParser.feed(sContents)
		hParser.close()
		
		self.aURLs	= hParser.get_urls()
		self.aWords	= hParser.get_words()		

	#
	# Parse the links out of a webpage for crawling
	#
	def parse_links(self, sContents):

		aLinks = re.findall("<a(.*)(href\=\"(.*)(\"))>(.*?)<\/a>", sContents)
		for aLink in aLinks:
			sURL	= aLink[2]
			print sURL
				

	#
	# Check if a value is already listed in an array
	#
	def array_value_exists(self, sNeedle, aHaystack):
		for sHaystack in aHaystack:
			if sHaystack == sNeedle:
				return True
			
		return False
		