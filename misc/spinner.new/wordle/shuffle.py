#
# Shuffle
#
# Shuffle some words yo'
#

class Shuffle(object):
	
	
	#
	# Join two dictionary sets together
	#	
	def word_join(self, kWords, aMatrix):

		aWords = []

		for sWord in kWords:
			aWords.append(sWord)
			for kMatrix in aMatrix:
				for sTmpWord in kMatrix['words']:
					aWords.append(sWord + sTmpWord)

		return aWords			

	
	#
	# Return the cream of the crop, or the highest rated words
	#
	def word_cream(self, kWords, bPercent = .4):
		
		aFinal	= []
		nLen		= len(kWords)
		nMax		= max(kWords.values())
		nNum		= int(round(bPercent * nLen))

		while nNum > 0 and nMax > 0:
			
			for sWord in kWords:
				
				if kWords[sWord] >= nMax and sWord not in aFinal:
					aFinal.append(sWord)
					nNum -= 1

				else:
					nMax -= 1
					
		return aFinal			
		
	
	#
	# Filter an entire matrix by creamyness
	#
	def filter(self, aMatrix):
		
		aFinal = []
		
		for kMatrix in aMatrix:
			aFinal.append(self.word_cream(kMatrix['words']))
			
		print aFinal
#		return aFinal
			
	#
	# Shuffle a list of words with associated types and weights
	#
	def shuffle(self, aMatrix):
		
		aMatrix = self.filter(aMatrix)
		print aMatrix
		
		i 			= 1
		aWords	=	[]

		for kMatrix in aMatrix:
			
			nType	 	= kMatrix['type']
			kWords	= kMatrix['words']
			sName		= kMatrix['name']
			
#			aWords.extend(self.word_join(kWords, aMatrix[i::]))

			i += 1	

		return aWords


	#
	# Sum a Dictionary on its values
	#
	def sum(self, kList):
		nTotal = 0
	
		for sWord in kList:
			nTotal += kList[sWord]
		
		return nTotal