import unittest
import MySQLdb
from instockdomains.spinner import models as spinner
from instockdomains import exceptions

class Basic(unittest.TestCase):

		def testOneWord(self):
				"""Test for one word. If you pass in 1 word you should get an array of
				words back that are synonymous"""

				spinner.Synonym.objects.add('directory', 'catalog', 10)
				spinner.Synonym.objects.add('list', 'directory', 20)
				spinner.Synonym.objects.add('directory', 'guide', 10)

				synonyms = spinner.Synonym.objects.get_synonyms(['directory'])
				assert len(synonyms) < 3, synonyms

		def testTwoWords(self):
				"""Test for two words. If you pass in a tuple of word pairs you should
				get a tuple of word pairs that are synonyms back"""

				words = ['business', 'directory']
				synonyms = spinner.Synonym.objects.get_synonyms(words)

				assert len(synonyms)

		def testKarma(self):
				"""Test if karma is approrpriately working"""

				spinner.Synonym.objects.add('directory', 'catalog', 10, True)
				spinner.Synonym.objects.add('list', 'directory', 20, True)
				spinner.Synonym.objects.add('directory', 'guide', 10, True)

				synonyms = spinner.Synonym.objects.get_synonyms(['directory'])[0]
				
				for word in synonyms:
						if word.total_karma < 10:
								assert False, 'Karma was not recorded correctly'

				

		def testWords(self):
				"""Test if we can add words individually"""

				words = ['mac', 'tips', 'tricks', 'macintosh', 'help', 'hack']

				for word in words:
						ref = spinner.Word.objects.get_single(word, True)
						assert isinstance(ref, spinner.Word)
						ref.delete()

		def testAddWords(self):
				"""Test if we can add words in bulk"""

				words = ['mac', 'tips', 'tricks', 'macintosh', 'help', 'hack']
				spinner.Word.objects.add(words)
				for word in words:
						word = spinner.Word.objects.get(name=word)
						word.delete()
		

		def testSynonym(self):
				"""Test if creating synonyms is working"""

				one = spinner.Word.objects.get_single('mac', True)
				two = spinner.Word.objects.get_single('macintosh', True)

				syn = spinner.Synonym.objects.get_single(one, two, True)
				assert isinstance(syn, spinner.Synonym), syn
				
				syn.delete()
				one.delete()
				two.delete()

		def testSynonymDuplicate(self):
				"""Test a regular duplicate synonym"""
				one = spinner.Word.objects.get_single('mac', True)
				two = spinner.Word.objects.get_single('macintosh', True)
	
				syn = spinner.Synonym.objects.get_single(one, two, True)
				
				syn2 = spinner.Synonym.objects.get_single(two, one, True)

				assert syn == syn2

				syn.delete()
				one.delete()
				two.delete()


		def testAddSyn(self):
				"""Helper function for adding synonyms"""

				syn = spinner.Synonym.objects.get_single('mac', 'macintosh')
				assert syn is None, syn

				syn = spinner.Synonym.objects.add('mac', 'macintosh', 5)
				assert isinstance(syn, spinner.Synonym), syn
				syn.delete()


		def testGetSingle(self):
				"""See if our get_single() synonym manager is working"""

				syn = spinner.Synonym.objects.get_single('mac', 'macintosh')
				assert syn == None
				

		def testGetSingleWordCreate(self):
				"""Check our get_single() for Word object"""

				word = spinner.Word.objects.get_single('mac', True)
				assert isinstance(word, spinner.Word), word
				word.delete()

				word = spinner.Word.objects.get_single('mac', True)
				assert isinstance(word, spinner.Word), word
				word.delete()

try:
		suite = unittest.TestSuite(map(Basic, tests))
		runner = unittest.TextTestRunner()
		runner.run(suite)
except NameError:
		unittest.main()
