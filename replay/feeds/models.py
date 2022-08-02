from django.core.cache import cache
from django.db import models
from django.http.response import Http404
from django.urls import reverse
from django.utils import timezone
from email.utils import format_datetime, parsedate_to_datetime
from urllib.parse import urlsplit, urlunsplit
from uuid import uuid4
import re
import requests


STYLESHEET_EX = r'\<\?xml-stylesheet[^\>]+\>'
PUBDATE_EX = r'\<pubDate\>([^\<]+)\</pubDate\>'
ITEM_EX = r'\<item[^\>]*\>(.+?)\</item\>'
GENERATOR_EX = r'\<generator\>([^\<]+)\</generator\>'
ITUNES_NEW_FEED_EX = r'\<itunes:new-feed-url\>([^\<]+)\</itunes:new-feed-url\>'
TITLE_EX = r'\<(itunes:)?title\>(?:\<!\[CDATA\[)?([^\<]+)</(itunes:)?title\>'
LAST_BUILD_DATE_EX = r'\<lastBuildDate\>([^\<]+)\</lastBuildDate\>'
ITUNES_BLOCK_EX = r'\<itunes:block\>([^\<]*)\</itunes:block\>'
ITUNES_EMAIL_EX = r'\<itunes:email\>([^\<]*)\</itunes:email\>'
MANAGING_EDITOR_EX = r'\<managingEditor\>([^\<]+)</managingEditor\>'  # NOQA


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.URLField('URL', max_length=512)
    start_date = models.DateTimeField(auto_now_add=True)
    last_fetched = models.DateTimeField(null=True)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('subscription_detail', args=(self.pk,))

    def get_feed_url(self):
        return reverse('subscription_feed', args=(self.pk,))

    def fetch_and_rewind(self, exclude_future=True, prefix_title=True):
        urlparts = list(urlsplit(self.url))
        secure_url = urlunsplit(['https', *urlparts[1:]])
        insecure_url = urlunsplit(['http', *urlparts[1:]])

        def rewind(match):
            item_date = parsedate_to_datetime(match.groups()[0])
            delta = item_date - first_date
            new_date = self.start_date + delta
            return '<pubDate>%s</pubDate>' % format_datetime(new_date)

        def cutoff(match):
            item = match.groups()[0]
            pubdate = re.search(PUBDATE_EX, item, re.MULTILINE)

            if pubdate is not None:
                pubdate = parsedate_to_datetime(pubdate.groups()[0])
                if pubdate > now:
                    return '<!-- Item scheduled for future release -->'

            return '<item>%s</item>' % item

        def retitle(match):
            prefix, title, suffix = match.groups()
            title = match.groups()[1]

            title = title.strip()
            if title.endswith(']]>'):
                title = title[:-3]

            return '<%stitle>⏪ %s</%stitle>' % (
                prefix or '', title, suffix or ''
            )

        def replace_editor(match):
            name = match.groups()[0]
            name_match = re.match(r'.+ \(([^\)]+)\)', name)

            if name_match is not None:
                return '<managingEditor>%s</managingEditor>' % (
                    name_match.groups()[0]
                )

            return name

        cachekey = 'feeds.%s' % self.pk
        content_type = None

        if cachekey not in cache:
            try:
                response = requests.get(secure_url)
            except requests.exceptions.SSLError:
                response = requests.get(insecure_url)

            if response.status_code == 404:
                raise Http404('Feed not found')

            response.raise_for_status()
            content_type = response.headers['content-type']
            content = response.content.decode('utf-8')
            cache.set(
                cachekey,
                (content_type, content),
                500
            )
        else:
            content_type, content = cache.get(cachekey)

        first_date = None
        for match in re.findall(PUBDATE_EX, content):
            date = parsedate_to_datetime(match)

            if first_date is None:
                first_date = date
            elif date < first_date:
                first_date = date

        content = re.sub(STYLESHEET_EX, '', content)
        now = timezone.now()
        content = re.sub(PUBDATE_EX, rewind, content)

        if exclude_future:
            content = re.sub(ITEM_EX, cutoff, content, flags=re.S)

        content = re.sub(
            GENERATOR_EX,
            '<generator>replay.origin.fm</generator>',
            content
        )

        if prefix_title:
            content = re.sub(TITLE_EX, retitle, content)

        content = re.sub(
            LAST_BUILD_DATE_EX,
            lambda match: '<lastBuildDate>%s</lastBuildDate>' % format_datetime(now),  # NOQA
            content
        )

        content = re.sub(ITUNES_NEW_FEED_EX, '', content)

        block_match = re.search(ITUNES_BLOCK_EX, content, re.S)
        if block_match is None:
            first_item_index = content.find('<item')
            before_first_item = content[:first_item_index]
            after_first_item = content[first_item_index:]
            content = (
                before_first_item +
                '<itunes:block>Yes</itunes:block>' +
                after_first_item
            )
        else:
            content = re.sub(
                ITUNES_BLOCK_EX,
                '<itunes:block>Yes</itunes:block>',
                content
            )

        content = re.sub(ITUNES_EMAIL_EX, '', content)
        content = re.sub(MANAGING_EDITOR_EX, replace_editor, content)

        self.last_fetched = now
        self.save(update_fields=('last_fetched',))

        return content_type, content

    class Meta:
        unique_together = ('start_date', 'url')
        ordering = ('url',)


class BlockedFeed(models.Model):
    url = models.URLField('URL', max_length=512)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Subscription.objects.filter(
            url__iexact=self.url
        ).delete()

    class Meta:
        ordering = ('url',)
