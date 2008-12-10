import unittest
from spinner import Spinner
	
class SpinnerTest(unittest.TestCase):
   				
		def testAssertCond(self):
			self.assert_(3 in range(4))
			
		def synonymsTest(self, sApp, xData):

			if sApp == 'boss':
				aResults 	= [result[0] for result in xData['results']]
				sPhrase 	= xData['phrase']
				nPage			= xData['page']

				assert len(aResults) == 50, len(aResults)
				
				if nPage is 0:
					assert len('wii sports cheats, codes, cheat codes for nintendo wii (nwii)') is len(aResults[13]), aResults[13]
					assert len('wii cheats, reviews, faqs, message boards, and more - gamefaqs') is len(aResults[0]), '"'+aResults[0]+'"'
					assert len('wii sports: cheats, cheat codes, tips & trainers! - cheating wii sports ...') is len(aResults[47]), '"'+aResults[47]+'"'				
					#self.oSpin.aDrivers[sApp].oResults

				self.assertEqual(sPhrase, 'wii tips')
			
				kSynonyms = self.oSpin.synonyms(aResults, True)
				
				for sWord, aSynonyms in kSynonyms.iteritems():
					print sWord, aSynonyms
					
		def testBoss(self):
			self.oSpin = Spinner()
			self.oSpin.search('wii tips', ['boss'], [self.synonymsTest])
