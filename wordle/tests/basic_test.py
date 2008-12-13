import unittest
from instockdomains import wordle

class Basic(unittest.TestCase):

		def testClean(self):
				"""Test the clean function"""

				phrase = 'this!@/.is!-a-!phrase'
				assert 'thisisaphrase' == wordle.clean(phrase), wordle.clean(phrase)

		def testGetSynonyms(self):
				"""Test the get synonyms function"""

				query = "mac tips"


try:
		suite = unittest.TestSuite(map(Basic, tests))
		runner = unittest.TextTestRunner()
		runner.run(suite)
except NameError:
		unittest.main()
