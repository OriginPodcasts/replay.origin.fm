from django.template import Library
from datetime import datetime
from email.utils import parsedate_to_datetime


register = Library()


@register.filter()
def isfuture(value):
    value_date = parsedate_to_datetime(value)
    now = datetime.now()

    if value_date.tzinfo:
        now = now.replace(tzinfo=value_date.tzinfo)

    return value_date > now


@register.filter()
def emaildate(value):
    return parsedate_to_datetime(value)
