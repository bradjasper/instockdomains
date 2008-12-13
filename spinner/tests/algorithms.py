"""Algorithms is a unittest that tests different types of algorithms for the
best way to generate synonyms."""
from spyder import proxy
import wordle
import pprint
import unittest

class Algorithms(unittest.TestCase):

    query = 'mac tips'

    def testBOSSFoldTitles(self):
        """This algorithm queries BOSS, gathers each result's title and folds
        the title into synonyms."""

        boss = proxy.BOSS()
        results = boss.get_results(self.query)
        titles = [wordle.clean(result['title']) for result in results]

        folder = wordle.TitleFolder()
        synonyms = folder.get_synonyms(titles, self.query)

        pprint.pprint(synonyms)

try:
		suite = unittest.TestSuite(map(Algorithms, tests))
		runner = unittest.TextTestRunner()
		runner.run(suite)
except NameError:
		unittest.main()
