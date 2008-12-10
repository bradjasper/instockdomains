#
# Weight
#
# A Wordle extension that divides messages into relative weights
#

import wordle

LEFT = 0
RIGHT = 1
CENTER = 2


class Weight(wordle.Wordle):
	
	#
	# Return a dictionary with sPhrase weights from aArray
	#
	def weight(self, sPhrase, aArray):

		aPhrase		= sPhrase.split(' ')
		kMatrix		= []

		for i in xrange(0, len(aPhrase)):
			sWord = aPhrase[i]
			nType = self.get_type(i, len(aPhrase))
			
			kMatrix.append({
				'name': sWord,
				'type':	nType,
				'words': self.splitter(sWord, aPhrase, aArray, nType)
			})
			

		print aArray, "\r\n\r\n"
		
		for x in kMatrix:
			print x, ' -- ',kMatrix[x]['words']


			
	#
	# Return the relative weight of a word to each item in the array
	#
	def splitter(self, sWord, aPhrase, aArray, nType):


		kFinal	= {}
		nDepth	= 4

		for sLine in aArray:

			nCurrent, aLine, kSlice = 0, sLine.split(' '), {}
			
			for sTmpWord in aLine:
				
				#	Word Matched
				if sTmpWord == sWord:
					kSlice	= self.slice(aLine, nType, nCurrent, nDepth)
					kFinal	= self.combine(kFinal, kSlice)
					
#					if len(kSlice):
#						print sWord,' -- ',sLine,' -- ',kFinal,' -- ',nType
					
				nCurrent += 1
				
		return kFinal

	
	#
	# Slice an array into the important parts
	#
	def slice(self, aArray, nType, nCurrent, nDepth):
		
		aSlices = []
		
		if nType == LEFT:
			nStart, nEnd = nCurrent+1, nCurrent+nDepth+1
			aSlices.append(aArray[nStart:nEnd])
			
		elif nType == RIGHT:
			nStart, nEnd = nCurrent-nDepth, nCurrent
			if nStart < 0: nStart = 0
			aSlices.append(aArray[nStart:nEnd][::-1])
			
		elif nType == CENTER:
			nDepth = int(round(nDepth/2))
			nStart, nEnd = nCurrent-nDepth, nCurrent+nDepth+1
			if nStart < 0: nStart = 0
			nMiddle = nCurrent - nStart
			
			aSlice = aArray[nStart:nEnd]
			aSlices.append(aSlice[nMiddle+1::])
			aSlices.append(aSlice[0:nMiddle][::-1])

		return self.calc_freq(aSlices, nDepth)
		

	#
	#	Calculate the frequency of an array item based on its position
	# 	- closer items are rated higher
	#
	def calc_freq(self, aArray, nDepth):
		kDict = {}

		for aList in aArray:
			for i in range(0, len(aList)):
				nScore	= nDepth - i
				sWord		= aList[i]

				if sWord in kDict.keys():
					kDict[sWord] += nScore
				else:
					kDict[sWord] = nScore

		return kDict
			

		
	#
	# Return the type of word it is positionally
	#		LEFT|RIGHT|CENTER
	#
	def get_type(self, x, y):
		if y == 1: return CENTER
		if x == 0: return LEFT
		elif x == y-1: return RIGHT
		return CENTER		