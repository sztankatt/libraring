from django.db import models
from django.utils.translation import ugettext_lazy as _


class Brainstorm(models.Model):
    name = models.CharField(max_length=63, verbose_name=_('Your name'))
    email = models.EmailField(verbose_name=_('Your e-mail'))
    comment = models.TextField(verbose_name=_('Comment'))
    datetime_posted = models.DateTimeField(auto_now_add=True)
