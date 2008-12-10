from django.db import connection, models
from django.contrib import admin
from django.shortcuts import get_object_or_404

#
#	Namespacing
#
class Space(models.Model):
	name	= models.CharField(max_length=100, unique=True)

	class Admin:
		pass

	def __unicode__(self):
		return self.name


#
#	Individual Word Model
#
class Word(models.Model):
	space			= models.ForeignKey(Space)
	name			= models.CharField(max_length=255, unique=True)
	karma			= models.IntegerField(default=0);
	relation	= models.ManyToManyField('self', through='Relation', symmetrical=True)
	
	class Admin:
		pass

	def __unicode__(self):
		return self.name
	
	class meta:
		unique_together = ('space', 'name')	
#
# Relationship Models
#
class RelationManager(models.Manager):
	#
	# Given a multi-dimensional array of synonyms,
	#	normalize_* will find any duplicates and add
	#	their karma's if necessary and return a single
	#	list of synonyms w/ karma
	#
	def normalize_synonyms(self, sWord, aSynonyms):
		
		kFinal = {}
		for aSyn in aSynonyms:
			nKarma, sWord1, sWord2 = aSyn
			
			if sWord == sWord1:
				sTmpWord = sWord2
			elif sWord == sWord2:
				sTmpWord = sWord1
			else:
				continue
				
			if sTmpWord in kFinal.keys():
				kFinal[sTmpWord] += nKarma
			else:
				kFinal[sTmpWord] = nKarma
				
		return kFinal
							
	#
	# This is our Synonym walk function. It takes a word and finds the synonyms.
	#
	def get_synonyms(self, aWords):

		aWhere = []
		for sWord in aWords:
			aWhere.append("(word1.name = '"+sWord+"' OR word2.name = '"+sWord+"')")
		sWhere = ' OR '.join(aWhere)

#			oWord = get_object_or_404(Word.objects.filter(name=sWord))
#			assert False, oWord.relation.filter()
#			assert False, Relation.relation.filter(rel_one=oWord)
#			oWords = Word.objects.get(name=sWord)
#			assert False, oWords.relation.filter(type=3)
		query = '''
SELECT DISTINCT relation.karma, word1.name, word2.name
FROM  `spinner_word` AS word1
INNER JOIN  `spinner_relation` AS relation ON relation.rel_one_id = word1.id
INNER JOIN  `spinner_word` AS word2 ON relation.rel_two_id = word2.id
WHERE relation.type = 3
AND (%s)
ORDER BY relation.karma DESC
''' % (sWhere)

		cursor = connection.cursor()
		cursor.execute(query)
		kSynonyms = {}
		for sWord in aWords:
			kSynonyms[sWord] = self.normalize_synonyms(sWord, cursor.fetchall())

		return kSynonyms
		
class RelationAdmin(admin.ModelAdmin):
	list_display = ('space', 'rel_one', 'rel_two', 'karma', 'gettype')


class Relation(models.Model):
	space		= models.ForeignKey(Space)
	rel_one	= models.ForeignKey(Word, related_name='related_one')
	rel_two	= models.ForeignKey(Word, related_name='related_two')	

	karma			= models.IntegerField(default=0)
	
	TYPE_CHOICES = (
		(0, 'One'),		#	One is the leading word. (mac => tips)
		(1,	'Two'),		#	Two is the leading word. (tips => tricks)
		(2, 'Both'),		# Center (maybe deprecated?)
		(3, 'Synonyms'),	#	Words can be used interchangebly (mac => apple)
	)
	
	type			= models.CharField(max_length=15, choices=TYPE_CHOICES, default=3)
	
	#	Python get/set properties--cool!
	def gettype(self): return self.TYPE_CHOICES[int(self.type)][1].lower()
	get_type	= property(gettype)

	objects		= RelationManager()
	class Admin:
		pass
		
	class meta:
		unique_together = ('rel_one', 'rel_two')

	def __unicode__(self):
		return "[%s] [%s] - %s / %s" % (self.space.name, self.TYPE_CHOICES[int(self.type)][1].lower(),
			self.rel_one.name, self.rel_two.name)


#admin.site.register(Space)
#admin.site.register(Word)
#admin.site.register(Relation, RelationAdmin)


