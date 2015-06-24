from django.forms import ModelForm
from django import forms

from books.models import Book, Author, Genre, Publisher, Offer

from django_select2.widgets import AutoHeavySelect2TagWidget, AutoHeavySelect2Widget
from django_select2.fields import AutoModelSelect2TagField, AutoModelSelect2Field, AutoSelect2Field

class AuthorWidget(AutoHeavySelect2TagWidget):
    def init_options(self):
        super(AuthorWidget, self).init_options()
        self.options['tokenSeparators'] = [","]

class AuthorField(AutoModelSelect2TagField):
    queryset = Author.objects
    search_fields = ['name__startswith']
    
    def get_model_field_values(self, value):
        return {'name': value}
    
class PublisherWidget(AutoHeavySelect2Widget):
    def init_options(self):
        super(AutoHeavySelect2Widget, self).init_options()
        self.options['tokenSeparators'] = [","]

class PublisherField(AutoModelSelect2Field):
    queryset = Publisher.objects
    search_fields = ['name__startswith']

    def extra_data_from_instance(self, obj):
        return {'aa':'bb'}
    
#TODO tokenseparators only ","
#TODO: Check if super(autoheavyselect2tagwidget) is the right thing to do
class GenreWidget(AutoHeavySelect2TagWidget):
    def init_options(self):
        super(GenreWidget, self).init_options()
        self.options['tokenSeparators'] = [","]

class GenreField(AutoModelSelect2TagField):
    queryset = Genre.objects
    search_fields = ['name__startswith']
    
    def get_model_field_values(self, value):
        return {'name': value}

g = GenreWidget(attrs={'type':''})

g.init_options()

#TODO: create an instance of authorwidget, and call init_options

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
    publisher = PublisherField(required=False)
    new_publisher = forms.CharField(label='Insert new Publisher', help_text='Insert new, if you can\'t \
        the Publisher in the search field above', required=False)
    isbn = forms.CharField(label='ISBN', required=False)
    includes_delivery_charges = forms.BooleanField(label='Price includes delivery charges', required=False)
    
    class Meta:
        model = Book
        exclude = ['user', 'upload_date', 'is_sold', 'sold_to']
        fields = [
                'title',
                'author',
                'edition',
                'genre',
                'price',
                'publisher',
                'new_publisher',
                'publication_year',
                'publication_city',
                'publication_country',
                'isbn',
                'image',
                'short_description',
                'includes_delivery_charges'
            ]
        help_texts = {
            'isbn':'Please key in a valid ISBN number',
            'edition': 'Please type-in the edition of the book'
        }

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        widgets = {
            'book':forms.HiddenInput(),
            'made_by': forms.HiddenInput()
        }

        exclude =['transaction', 'accepted']
    
