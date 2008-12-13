import unittest

import wordle

class Basic(unittest.TestCase):

		def testClean(self):
				"""Test the clean function"""

				phrase = 'this!@/.is!-a-!phrase'
				assert 'this-is-a-phrase' == wordle.clean(phrase), wordle.clean(phrase)

		def testMatchSynonyms(self):
				"""Test the get synonyms function"""

                query = "mac tips"
                data = ['mac tips, tricks, hacks', 'mac users and stuff',
                        'macintosh tips and apple tips',
                        'osx tips, tricks, hacks']

                wordle = wordle.TitleFolder()
                wordle.match_synonyms(data, query)


try:
		suite = unittest.TestSuite(map(Basic, tests))
		runner = unittest.TextTestRunner()
		runner.run(suite)
except NameError:
		unittest.main()
