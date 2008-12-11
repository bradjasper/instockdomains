import datetime
from django.db import models
from instockdomains import exceptions
import MySQLdb

class	CommonBase(models.Model):
		"""Base class for holding meta data like dates and active"""

		created_date = models.DateTimeField()
		modified_date =	models.DateTimeField()

		active =	models.BooleanField(default=1)
		karma = models.IntegerField(default=1)

		class Meta:
				abstract = True

		def save(self):
				if not self.created_date:
						self.created_date = datetime.datetime.now()

				self.modified_date = datetime.datetime.now()
				super(CommonBase, self).save()


class WordManager(models.Manager):

		def get_single(self, name, create = None):
				"""Return a single word. If create is True, one will be created if it
				doesn't exist"""

				if create is None:
						create = False

				try:
						return self.get(name=name)

				except Word.DoesNotExist:
						if create:
								word = Word(name=name)
								word.save()
								return word
				return None

		def add(self, words):
				"""Add a set of words into the list database and return a reference to
				each"""

				for name in words:
						try:
								word = self.get(name=name)
						except Word.DoesNotExist:
								word = Word(name=name)
								word.save()
								
class Word(CommonBase):
		name = models.CharField(max_length=255, unique=True)
		objects = WordManager()

		def __unicode__(self):
				return self.name


class SynonymManager(models.Manager):


		def add(self, word_one, word_two, karma = None, update = None):
				"""Lazily add two words as synonyms. If update, the karma's
				are added"""

				if karma is None:
						karma = 1

				if update is None:
						update = False

				syn = self.get_single(word_one, word_two)

				if isinstance(syn, Synonym):
						if update:
								syn.karma += karma
								syn.save()
				else:
						try:
								one = Word.objects.get_single(word_one, True)
								two = Word.objects.get_single(word_two, True)
								syn = Synonym(word_one=one, word_two=two)
								syn.karma = karma
								syn.save()
						except:
								raise

				return syn

		def get_single(self, word_one, word_two, create = None):
				"""Check to see if word_one, word_two or word_two, word_one match"""

				if create is None:
						create = False

				syn = None
				try:
						syn = Synonym.objects.get(word_one=word_one, word_two=word_two)
				except (MySQLdb.IntegrityError, Synonym.DoesNotExist):
						try:
								syn = Synonym.objects.get(word_one=word_two, word_two=word_one)
						except (MySQLdb.IntegrityError, Synonym.DoesNotExist):
								if create:
										syn = Synonym(word_one=word_one, word_two=word_two)
										syn.save()

				return syn


		def exists(self, word_one, word_two):
				"""Check to see if a pair of words have any existing matches"""

				return isinstance(self.get_single(word_one, word_two), Word)


class Synonym(CommonBase):

		word_one = models.ForeignKey(Word, related_name='First word')
		word_two = models.ForeignKey(Word, related_name='Second word')
		objects = SynonymManager()

		def __unicode__(self):
				return "%s - %s - %d" % (unicode(self.word_one),
								unicode(self.word_two), self.karma)

		class Meta:
				unique_together = ('word_one', 'word_two')

		def save(self):
				if not self.created_date:
						if Synonym.objects.exists(self.word_one, self.word_two):
							raise exceptions.DuplicateError('Synonym already exists')

				CommonBase.save(self)
