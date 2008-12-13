import unittest
import json
from instockdomains.spyder import proxy
import pprint

class Basic(unittest.TestCase):

		def testWordnetSynonyms(self):
				"""Test WordNet synonyms"""
				wordnet = proxy.WordNet()
				results = wordnet.synonym('business directory')

		def testBossQuery(self):
				"""Make sure BOSS query is working"
				boss = proxy.BOSS()
				results = boss.query('domain names')
				assert 'ysearchresponse' in results.keys(), results
				assert results['ysearchresponse']['count']

		def testBossResults(self):
				"""Get the BOSS results/keyterms back"""
				boss = proxy.BOSS()
				results = boss.get_results('directory')
				words = {}
				titles = []
				for result in results:
						terms = result['keyterms']['terms']
						titles.append(result['title'])
						for term in terms:
								term = term.lower()
								curr = words.get(term, 0)
								curr += 1
								words[term] = curr

				words = sorted(words.iteritems(), key=lambda (x,y): (y,x),
						reverse=True)
				pprint.pprint(words[:20])
				print ""
				pprint.pprint(titles)
#						print result['title'].encode('UTF-8')
#						print "--"

		def testGetKeyterms(self):
				"""Get the BOSS keyterms back"""
				boss = proxy.BOSS()
				keyterms = boss.get_keyterms('mac tips')
				assert len(keyterms)

		def testGetTitles(self):
				"""Get the BOSS titles back"""
				boss = proxy.BOSS()
				titles = boss.get_titles('mac tips')
				assert len(titles)

tests = ['testWordnetSynonyms']

try:
		suite = unittest.TestSuite(map(Basic, tests))
		runner = unittest.TextTestRunner()
		runner.run(suite)
except NameError:
		unittest.main()
