from django.test import TestCase, Client
from books.forms import BookForm
from books.models import Author, Genre, Publisher, Book, Offer
from django.contrib.auth.models import User
from usr.models import Person
from usr.project import confirmation_code_generator

import datetime


class BookTestCase(TestCase):

    def setUp(self):
        # setting up genres and authors
        genres = [
            'international relations', 'mathematics', 'physics',
            'history', 'politics', 'sociology']

        authors = [
            'George Orwell', 'William Shakespeare']

        self.genre_objects = []
        self.author_objects = []

        for genre in genres:
            g = Genre.objects.create(name=genre)
            self.genre_objects.append(g)

        for author in authors:
            a = Author.objects.create(name=author)
            self.author_objects.append(a)

        # creating location
        # setting up users and persons
        self.foo = User.objects.create_user(
            username='foo', password='foo', email='foo@foo.com')
        self.bar = User.objects.create_user(
            username='bar', password='bar', email='bar@bar.com')

        u1 = User.objects.create_user(
            username='user1', password='asd', email='aa@gmail.com')

        u2 = User.objects.create_user(
            username='user2', password='wasd', email='bb@gmail.com')

        Person.objects.create(
            user=self.foo,
            title='MR',
            confirmation_code=confirmation_code_generator(),
            block_code=0)

        Person.objects.create(
            user=self.bar,
            title='MS',
            confirmation_code=confirmation_code_generator(),
            block_code=0)

        Person.objects.create(
            user=u1,
            title='MRS',
            confirmation_code=confirmation_code_generator(),
            block_code=0)

        Person.objects.create(
            user=u2,
            title='MR',
            confirmation_code=confirmation_code_generator(),
            block_code=0)

        # Creating Books
        b1 = Book.objects.create(
            title='Hamlet',
            price=20,
            publication_year=2001,
            user=self.foo,
            edition=2,
            upload_date=datetime.datetime.now(),
            )

        b1.genre.add(self.genre_objects[3])
        b1.genre.add(self.genre_objects[5])
        b1.author.add(self.author_objects[1])
        b1.save()

        b2 = Book.objects.create(
            title='1984',
            price=11,
            edition=1,
            publication_year=1948,
            user=self.bar,
            upload_date=datetime.datetime.now(),
            )

        b2.genre.add(self.genre_objects[0])
        b2.genre.add(self.genre_objects[4])
        b2.author.add(self.author_objects[0])
        b2.save()

        # creating offer for b2
        self.offer1 = Offer.objects.create(
            book=b2,
            offered_price=10,
            made_by=u1,
            accepted=False)

        self.offer2 = Offer.objects.create(
            book=b2,
            offered_price=15,
            made_by=u2,
            accepted=False)

        self.client = Client()

    def test_uploading(self):
        data = {
            'title': u'Title',
            'author': [u'aa'],
            'genre': [Genre.objects.get(name='international relations').pk],
            'publication_year': u'2010',
            'edition': 1,
            'price': u'20',
            'new_publisher': u'new_publisher'
        }

        form = BookForm(data)

        if form.is_valid():

            book = form.save(commit=False)

            new_publisher = form.cleaned_data['new_publisher']
            if book.publisher == None and new_publisher != "":
                p = Publisher(name=new_publisher)
                p.save()

            book.publisher = p

            book.user = self.foo
            book.upload_date = datetime.datetime.now()
            book.save()
            form.save_m2m()

    def test_book_methods(self):
        b = Book.objects.get(title='Hamlet')

        self.assertEqual(b.title, 'Hamlet')
        self.assertEqual(b.accepted_offer(), None)
        self.assertEqual(b.get_location().city, 'Cambridge')
        self.assertEqual(b.is_sold(), False)
        self.assertEqual(b.is_finalised(), False)
        self.assertEqual(b.get_highest_offer(), None)
        self.assertEqual(b.get_watchlist_users(), [])
        self.assertEqual(b.get_offer_users(), [])

    def test_login(self):
        self.assertTrue(self.client.login(username='foo', password='foo'))

    def test_make_an_offer_clean(self):
        self.client.login(username='user1', password='asd')
        response = self.client.post('/en/books/make/an/offer/', {})
        self.assertEqual(response.status_code, 404)

    def test_make_an_offer_correct(self):
        self.client.login(username='user1', password='asd')
        book = Book.objects.get(title='1984')
        response = self.client.post(
            '/en/books/make/an/offer/',
            {
                'made_by': User.objects.get(username='user1').pk,
                'book': book.pk,
                'offered_price': 20
            }
        )

        self.assertRedirects(
            response,
            '/en/books/book/'+str(Book.objects.get(title='1984').pk)+'/'
        )

        self.assertEqual(book.get_highest_offer().offered_price, 20)

        self.client.logout()

    def test_make_an_offer_new_user(self):
        self.client.login(username='foo', password='foo')
        book = Book.objects.get(title='1984')
        user = User.objects.get(username='foo')
        response = self.client.post(
            '/en/books/make/an/offer/',
            {
                'made_by': user.pk,
                'book': book.pk,
                'offered_price': 30
            }
        )

        self.assertRedirects(
            response,
            '/en/books/book/'+str(book.pk)+'/')

        self.assertEqual(book.get_highest_offer().offered_price, 30)
        self.assertTrue(user in book.get_offer_users())
        self.assertTrue(user == book.get_highest_offer().made_by)

        self.client.logout()

    def test_book_status_change(self):
        self.client.login(username='bar', password='bar')
        book = Book.objects.get(title='Hamlet')
        user = User.objects.get(username='bar')
        self.assertEqual(book.status, 'normal')

        response = self.client.post(
            '/en/books/make/an/offer/',
            {
                'made_by': user.pk,
                'book': book.pk,
                'offered_price': 20
            }
        )

        self.assertRedirects(
            response,
            '/en/books/book/'+str(book.pk)+'/')

        book = Book.objects.get(title='Hamlet')

        self.assertEqual(book.status, 'offered')

        self.client.logout()

    def test_accept_the_offer(self):
        self.client.login(username='foo', password='foo')
        book = Book.objects.get(title='1984')

        url = '/en/books/accept/the/offer/'

        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(url, {'offer_id': 40})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(url, {'offer_id': 2})
        self.assertEqual(response.status_code, 404)

        self.client.logout()
        self.client.login(username='bar', password='bar')

        self.assertEqual(book.accepted_offer(), None)

        response = self.client.post(url, {'offer_id': 2})
        self.assertRedirects(response, '/en/books/book/'+str(book.pk)+'/')

        book = Book.objects.get(title='1984')
        self.assertTrue(book.status == 'selling')

        self.assertEqual(book.accepted_offer().pk, 2)
