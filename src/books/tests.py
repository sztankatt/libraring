from django.test import TestCase
from books.forms import BookForm
from books.models import *

import datetime

class BooksTestCase(TestCase):
	def setUp(self):
		Genre.objects.create(name='international relations')
		Author.objects.create(name='testauthor')
		Publisher.objects.create(name='aa')
		User.objects.create(username='tomooka', password='1234')

	def test_uploading(self):
		data = {
			'title':u'Title',
			'author':[u'aa'],
			'genre':[Genre.objects.get(name='international relations').pk],
			'publication_year':u'2010',
			'edition':1,
			'price':u'20',
			'new_publisher':u'new_publisher'
		}

		form = BookForm(data)

		if form.is_valid():

			book = form.save(commit=False)

			new_publisher = form.cleaned_data['new_publisher']
			if book.publisher == None and new_publisher != "":
				p = Publisher(name=new_publisher)
				p.save()

				book.publisher = p

			book.user = User.objects.get(username='tomooka')
			book.upload_date = datetime.datetime.now()
			book.save()
			form.save_m2m()

			for genre in book.genre.all():
				print(genre.name)


	#def test_author_creation(self):
	#	Author.objects.create(name='testauthor')

	def test_long_genre(self):
		Genre.objects.create(name='this name is too long')

