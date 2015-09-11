from django.db import models
from django.contrib.auth.models import User

from books.models import Transaction


class Message(models.Model):
    transaction = models.ForeignKey(Transaction)
    sender = models.ForeignKey(User)
    text = models.TextField()
    send_date = models.DateTimeField()
    seen = models.BooleanField(default=False)
