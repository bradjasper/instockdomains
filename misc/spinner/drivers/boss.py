
#
# BOSS
#
# Yahoo BOSS API Search Engine
#

import base, urllib, simplejson, re
from spinner import toolbox
from wordle import wordle
from spinner import signals

class Boss(base.Base):
	
	API_KEY		= 'rcIUhrnV34FUR8oMfz_FW1WLg5z3vMutyAy3LcUtJ8pxe8Tw2Apf9dyhi5VVocf5'	
	API_URL		= 'http://boss.yahooapis.com/ysearch/web/v1/%s?appid=%s&count=50&start=%s' % ('%s', API_KEY, '%s')

	nMax			= 150

	#
	# Search for a keyword using BOSS
	#
	def search(self, sPhrase, aCallbacks, **kwargs):
		bExtended	= kwargs.get('extended', False)
		bDebug		= kwargs.get('debug', False)
		nPages		= int(round(self.nMax / 50))
		

		for nCurr in range(0, nPages-1):
			sURL 				= self.get_api_url(sPhrase, nCurr * 50)
			oQuery			= urllib.urlopen(sURL)
		
			sContents		= oQuery.read()
			oResults		= simplejson.loads(sContents)
			oReturn			=	{
				'phrase':	sPhrase,
				'page': nCurr,
				'results': []
			}
		
			oQuery.close()		

			for oResult in oResults['ysearchresponse']['resultset_web']:
				oReturn['results'].append( self.sanitize(oResult['title']) )
		
				if bExtended:
					oReturn['results'].append( self.sanitize(oResult['abstract']) )

				
			for oCallback in aCallbacks:
				oCallback('boss', oReturn)
				

		
	
	#
	# Sanitize a title
	#
	def sanitize(self, sTitle):
		
		sTitle		= sTitle.encode('UTF-8')
		oToolbox	= toolbox.Toolbox()
		sTitle		= oToolbox.strip_html(sTitle).lower()

		return [sTitle]

	#
	# 
	#
	def get_api_url(self, sPhrase, nStart):
		return self.API_URL % (urllib.quote(sPhrase), nStart)