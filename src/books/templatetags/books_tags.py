from django import template
from django.template.loader import get_template
from django.template import Context

register = template.Library()


@register.filter(name='star_rating')
def star_rating(rating):
    template = get_template('after_login/books/templatetags/star_rating.html')
    number = int(rating)

    half = 0

    if (rating - number) >= 0.5:
        half = 1

    remaining = 5-number

    stars = number*[1.0] + [0.5]*half + remaining*[0.0]

    c = Context({'stars': stars})

    content = template.render(c)

    return content
