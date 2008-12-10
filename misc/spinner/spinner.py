#
# Spinner
#
# Spinner is a manager for transforming words
#
# It's job is to hand a phrase off to a driver
# which generates more words based on the driver
#
# @author	Brad Jasper	<bjasper@gmail.com>
#
#
import os, glob, threading, re
from wordle import weight, wordle
from models import Word, Space, Relation

class Spinner(threading.Thread):
	
	aIgnore		= 'and for in its br com net a at ill nbsp the by of at all the more from org with'.split(' ')
	aDrivers	= {}
	sExact		= ''
	aResults	= []
	
	#
	# Load a set of drivers to use
	#
	# If you don't pass any drivers it loads them all
	#
	def load_drivers(self, aDrivers):
		for sDriver in aDrivers:
			if os.path.isfile(os.getcwd() + '/spinner/drivers/%s.py' % (sDriver)):
				exec("from drivers import " + sDriver)
				exec("self.aDrivers['%s'] = %s.%s()" % (sDriver, sDriver, sDriver.capitalize()))
		
	#
	# Take a phrase and pass it to the various
	# drivers we have
	#
	def search(self, sPhrase, aDrivers, aCallbacks):
		
		if len(aDrivers):
			self.load_drivers(aDrivers)
					
			for sDriver in aDrivers:
				oDriver = self.aDrivers[sDriver]
				oDriver.search(sPhrase, aCallbacks)



	#
	# Combine two dictionaries adding their common properties, assigning a weight to the heavier items
	#
	# Ex. {'tips': ['tricks', 'hacks', 'help'], 'tips': ['tricks', 'help']}
	#				=> {'tips':
	#						{
	#							'tricks':
	#									{'weight': 2},
	#							'help':
	#									{'weight': 2},
	#							'hacks':
	#									{'weight': 1}
	#						}
	#
	def weight_combine(self, kSynonyms, kFinal):
		
		if kFinal == None:
			kFinal = {}
			
		sWord			= kSynonyms.keys()[0]
		kWeights	= self.array_to_weight(kSynonyms[sWord], True)

		for sSyn in kWeights:
			
	
			if sSyn in kFinal.keys():
				kFinal[sSyn] = wordle.Wordle().combine(kFinal[sSyn], kWeights[sSyn])
		
			else:
				kFinal[sSyn] = kWeights[sSyn]

		return kFinal

	
	#
	# Convert an array to its relative weight
	#
	# Ex. ['this', 'is', 'an', 'array']
	#				=> {'this': 4,
	#						'is': 3,
	#						'an': 2,
	#						'array': 1
	#					}
	#
	def array_to_weight(self, aWords, bSame = False):
		
		kWeight = {}
		
		nCur = len(aWords) - 1
		while (nCur >= 0):
			if bSame: nWeight = 1
			else: nWeight = nCur+1
			kWeight[aWords[nCur]] = {'weight': nWeight}
			nCur -= 1
			
		return kWeight
	


	#
	# Fold a title into its relative synonyms
	# These are generally seperated by "and", "&" and ","
	#
	# Ex. mac tips, tricks, hacks and help 	=> {'tips': ['tricks', 'hacks', 'help']}
	#
	def fold_synonyms(self, sTitle):

		sTitle  = re.sub('(and|\&|\/)', ',', sTitle)

		aParts	= re.split('\,', sTitle)
		aWords	= []

		if len(aParts) > 1:

			sWord		= aParts.pop(0).strip().split(' ')[-1]			

			if len(sWord) < 2:
				return None

			for nCurr, sTmpWord in enumerate(aParts):
				sTmpWord 	= re.sub('[^a-zA-Z ]', '', sTmpWord).strip()
				aTmpWords = re.split(' ', sTmpWord)
				
				# Decide how words with spaces should be setup
				if len(aTmpWords) is 1:
					nIndex = 0
				else:
					if nCurr == len(aParts)-1:
						nIndex = 0
					else:
						nIndex = len(aTmpWords)-1						
					
				sTmpWord = aTmpWords[nIndex]
				
				if (sTmpWord not in self.aIgnore) and (sTmpWord not in aWords and len(sTmpWord) > 2):
						aWords.append(sTmpWord)


			if len(aWords):				
				return {sWord: aWords}

		return None		
	#
	#	Turn an array of titles into a dictionary of synonyms with relative weights
	#
	# Ex. ['mac tips, tricks and hacks', 'mac, apple, macintosh']
	#					=> {
	#								'tips': ['tricks', 'hacks'],
	#								'mac': ['apple', 'macintosh']
	#						}
	#
	def synonyms(self, aResults, bSave = True):
		
		sSpace	= 'global'
		kSyns		= {}
		
		for sTitle in aResults:

			kSyn = self.fold_synonyms(sTitle)
			
			if kSyn != None:
				
				sWord = kSyn.keys()[0]
				
				if not self.clean_word_check(sWord):
					continue
					
				if sWord not in kSyns.keys():
					kSyns[sWord] = {}
				
				kSyns[sWord] = self.weight_combine(kSyn, kSyns[sWord])

		kSyns = self.weight_clean(kSyns)
		
		if bSave:
			#	Store the results in our global namespace
			self.add_synonyms(kSyns, sSpace)
		
		return kSyns
		
	
	
	#
	# Perform various checks on a word to see if we want it
	# this generally includes special characters, numbers, etc...
	#
	def clean_word_check(self, sWord):
		
		sWord = sWord.lower()
		
		if len(sWord) <= 2:
			return False
			
		if re.match('[^a-z]', sWord):
			return False
		
		if sWord in self.aIgnore:
			return False
		
		return True
		
	#
	# Add any new synonyms to the database and 
	#	update any new ones with the added karma
	#
	# This could probably be a little cleaner
	#
	def add_synonyms(self, kSynonyms, sSpace = 'global'):
		
		try:
			oSpace = Space.objects.get(name=sSpace)
		except Space.DoesNotExist:
			oSpace = Space(name='global')
			oSpace.save()
			


		for sWord, kSyns in kSynonyms.iteritems():

			try:
				oWord = Word.objects.get(name=sWord, space=oSpace)
			except Word.DoesNotExist:
				oWord	= Word(name=sWord, space=oSpace)
				oWord.save()
				
			for sSyn, kProps in kSyns.iteritems():
				
				try:
					oSyn = Word.objects.get(name=sSyn, space=oSpace)
				except Word.DoesNotExist:
					oSyn = Word(name=sSyn, space=oSpace)
					oSyn.save()
					
				try:
					oRelation = Relation.objects.get(rel_one=oWord, rel_two=oSyn)
					oRelation.karma += kProps['weight']
					oRelation.save()
					
				except Relation.DoesNotExist:
					
					try:
						oRelation = Relation.objects.get(rel_two=oWord, rel_one=oSyn)
						oRelation.karma += kProps['weight']
						oRelation.save()
						
					except Relation.DoesNotExist:
						oRelation = Relation(rel_one=oWord, rel_two=oSyn, karma=kProps['weight'], space=oSpace)
						oRelation.save()
						
	
	#	Do a final clean-up to neatly arrange duplicates
	# Ex. tips tricks 4
	# 		tricks tips 2
	#			=> tips tricks 6
	def weight_clean(self, kSynonyms):
		
		kFinal = {}		
		
		for sWord, kSyns in kSynonyms.iteritems():			
			for sTestWord in kSyns:

				if sTestWord in kFinal.keys():
					if sWord in kFinal[sTestWord].keys():
						kFinal[sTestWord][sWord] = wordle.Wordle().combine(kFinal[sTestWord][sWord], kSyns[sTestWord])
					else:
						kFinal[sTestWord][sWord] = kSyns[sTestWord]
				else:
					
					if sWord not in kFinal.keys():
						kFinal[sWord] = {}
					
					kFinal[sWord][sTestWord] = kSyns[sTestWord]

		return kFinal