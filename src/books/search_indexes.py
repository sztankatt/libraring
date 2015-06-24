from haystack import indexes
from books.models import Book

import datetime

class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #title = indexes.CharField(model_attr='title')
    #author = indexes.CharField(model_attr='author')
    
    def get_model(self):
        return Book
    
    def index_queryset(self, using=None):
        return  self.get_model().objects