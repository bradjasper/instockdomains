import unittest
from spinner import spinner
	
class SpinnerTest(unittest.TestCase):
   				
		def setUp(self):
			self.oSpin = spinner.Spinner()

		def testAssertCond(self):
			self.assert_(3 in range(4))

						
		def testBoss(self):
			
			def callback(sApp, xData):
				
				if sApp == 'boss':
					self.aResults = xData['results']
					self.sPhrase 	= xData['phrase']
					
					self.assertEqual(len(self.aResults), 155)
					self.assertEqual(self.sPhrase, 'wii tips')
					
					kSynonyms = self.oSpin.synonyms(self.aResults)
					for sWord, aSynonyms in kSynonyms.iteritems():
						print sWord, aSynonyms
#					print len(aSynonyms)

		
			self.oSpin.search('wii tips', callback, 'boss')
#			print self.oSpin.fold_synonyms(
			
			
		
			  
#if __name__ == '__main__':
#	unittest.main()

def callback(sApp, xData):
	
	if sApp == 'boss':
		aResults = xData['results']
		sPhrase 	= xData['phrase']
		
		kSynonyms = oSpinner.synonyms(aResults)
		
		kPhrases	= oSpinner.phrases(aResults)
	
oSpinner = spinner.Spinner()
oSpinner.search(raw_input('>') or 'mac tips', callback)
