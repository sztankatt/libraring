import operator

from django.forms import ModelForm
from django import forms
from django.db.models import Count

from books.models import Book, Author, Genre, Publisher, Offer
from books.models import BOOK_STATUS_OPTIONS

from django_select2.widgets import AutoHeavySelect2TagWidget
from django_select2.fields import AutoModelSelect2TagField


class AuthorWidget(AutoHeavySelect2TagWidget):
    def init_options(self):
        super(AuthorWidget, self).init_options()
        self.options['tokenSeparators'] = [","]


class AuthorField(AutoModelSelect2TagField):
    queryset = Author.objects
    search_fields = ['name__startswith']

    def get_model_field_values(self, value):
        return {'name': value}


class PublisherWidget(AutoHeavySelect2TagWidget):
    def init_options(self):
        super(PublisherWidget, self).init_options()
        self.options['tokenSeparators'] = [","]


class PublisherField(AutoModelSelect2TagField):
    queryset = Publisher.objects
    search_fields = ['name__startswith']

    def get_model_field_values(self, value):
        return {'name': value}


class GenreWidget(AutoHeavySelect2TagWidget):
    def init_options(self):
        super(GenreWidget, self).init_options()
        self.options['tokenSeparators'] = [","]


class GenreField(AutoModelSelect2TagField):
    queryset = Genre.objects
    search_fields = ['name__startswith']

    def get_model_field_values(self, value):
        return {'name': value}


class BookForm(ModelForm):
    author = AuthorField(
        label='Author(s)',
        widget=AuthorWidget(
            select2_options={
                "placeholder": "Search authors",
            }
        ),
    )
    genre = GenreField(widget=GenreWidget())
    publisher = PublisherField(widget=PublisherWidget(), required=False)

    class Meta:
        model = Book
        fields = [
                'title',
                'author',
                'genre',
                'publisher',
                'publication_year',
                'price',
                'image'
            ]


class DetailedBookForm(forms.ModelForm):
    author = AuthorField(
        label='Author(s)',
        widget=AuthorWidget(
            select2_options={
                "placeholder": "Search authors",
            }
        ),
    )
    genre = GenreField(widget=GenreWidget())
    publisher = PublisherField(widget=PublisherWidget(), required=False)

    class Meta:
        model = Book
        exclude = [
                'sold_to',
                'status',
                'user',
            ]


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        widgets = {
            'book': forms.HiddenInput(),
            'made_by': forms.HiddenInput()
        }

        exclude = ['transaction', 'accepted']


class GenreForm(forms.Form):
    genre_query = Genre.objects.annotate(
        number_of_books=Count('book')).order_by('-number_of_books')[:10]
    genre_query = sorted(genre_query, key=operator.attrgetter('name'))
    GENRE_CHOICES = [(x, x) for x in genre_query]

    genres = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=GENRE_CHOICES)


class BookStatusForm(forms.Form):
    book_status = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=BOOK_STATUS_OPTIONS)
