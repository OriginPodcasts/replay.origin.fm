from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import DetailView, View
from replay import directories
from replay.seo.mixins import SEOMixin
from .models import Subscription, BlockedFeed
import feedparser


class CreateSubscriptionView(View):
    def post(self, request):
        url = directories.find(request.POST.get('url'))
        feed = feedparser.parse(url)
        blocked = BlockedFeed.objects.filter(url__iexact=url).exists()

        if any(feed.entries) and not blocked:
            obj = Subscription.objects.create(url=url)
            return HttpResponseRedirect(obj.get_absolute_url())

        return TemplateResponse(
            request,
            'feeds/feed_invalid.html',
            {
                'url': url,
                'seo_title': 'Feed invalid',
                'blocked': blocked
            },
            status=400
        )


class SubscriptionDetialView(SEOMixin, DetailView):
    model = Subscription
    template_name = 'feeds/subscription_detail.html'

    def get_context_data(self, **kwargs):
        content_type, feed = self.object.fetch_and_rewind(
            exclude_future=False,
            prefix_title=False
        )

        feed = feedparser.parse(feed)

        return {
            'feed': feed,
            'entries': sorted(
                list(feed.entries),
                key=lambda item: item.published_parsed
            ),
            'url': self.request.build_absolute_uri(
                self.object.get_feed_url()
            ),
            **super().get_context_data(**kwargs)
        }


class SubscriptionFeedView(View):
    def get(self, request, **kwargs):
        obj = get_object_or_404(Subscription, pk=kwargs['pk'])
        content_type, content = obj.fetch_and_rewind()

        return HttpResponse(
            content_type=content_type,
            content=content
        )
