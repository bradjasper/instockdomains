from instockdomains import wordle
import urllib
import json

class Base(object):
		pass


class Wordnet(Base):

		def __init__(self):
				#	This is such a heavy hit we only load it when necessary
				from nltk import wordnet

				Base.__init__(self)

		def get_synonyms(self, query):
				"""Query the Wordnet Dict's, return the words"""

				words = query.split()



class BOSS(Base):

		def query(self, query):
				"""Send BOSS a query, return the JSON"""

				url = self._get_api_url(query)
				query = urllib.urlopen(url)
				response = query.read()
				query.close()

				return json.loads(response)


		def _get_api_url(self, query):
				url = 'http://boss.yahooapis.com/ysearch/web/v1/%s?count=50&appid=%s&view=keyterms'
				key = 'rcIUhrnV34FUR8oMfz_FW1WLg5z3vMutyAy3LcUtJ8pxe8Tw2Apf9dyhi5VVocf5'
				return url % (urllib.quote(query), key)


		def get_results(self, query):
				"""Return the JSON resultset_web results"""
				response = self.query(query)
				return response['ysearchresponse']['resultset_web']


		def get_keyterms(self, query):
				"""Return the keyterms from the view"""
				results = self.get_results(query)
				return [result['keyterms']['terms'] for result in results]

		def get_titles(self, query):
				"""Given a query term, return a list of titles"""
				results = self.get_results(query)
				return [result['title'] for result in results]

