"""
		Classifiers have features. Features are interesting things about text that
		make it good/bad/unique/etc...

		Feature extraction function that defines what should go in the dictionary

		This is a basic classifier with a basic feature
"""


from nltk.classify import naivebayes
from nltk.classify.util import names_demo

def name_features(name):
		features = {}
		features['end-in-vowel'] = name.lower()[-1] in 'aeiouy'
		features['length'] = len(name)
		return features

classifier = names_demo(naivebayes.NaiveBayesClassifier.train, name_features)
