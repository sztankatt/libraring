from haystack import indexes
from books.models import Book
import queued_search

import datetime

class BookIndex(queued_search.indexes.QueuedSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Book
    
    def index_queryset(self, using=None):
        return  self.get_model().objects