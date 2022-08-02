from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files import File
from django.urls import reverse
from django.utils.safestring import mark_safe
import json
import os


class SEOMixin(object):
    seo_title = ''
    seo_description = ''
    robots = ''

    def get_seo_title(self):
        return self.seo_title

    def get_seo_description(self):
        return self.seo_description

    def get_canonical_url(self):
        if hasattr(self, 'canonical_url'):
            return self.request.build_absolute_uri(
                reverse(self.canonical_url)
            )

    def get_robots(self):
        return self.robots

    def get_context_data(self, **kwargs):
        return {
            'seo_title': self.get_seo_title(),
            'seo_description': self.get_seo_description(),
            'robots_content': self.get_robots(),
            'canonical_url': self.get_canonical_url(),
            **super().get_context_data(**kwargs)
        }


class OpenGraphMixin(object):
    og_locale = 'en-GB'
    og_type = 'article'
    og_title = 'Origin'
    og_description = ''
    og_site_name = 'Origin'

    twitter_card = 'summary_large_image'
    twitter_title = ''
    twitter_description = ''
    twitter_site = '@OriginPodcasts'
    twitter_creator = '@amarksteadman'

    def get_og_locale(self):
        return self.og_locale

    def get_og_type(self):
        return self.og_type

    def get_og_title(self):
        return self.og_title

    def get_og_description(self):
        return self.og_description

    def get_og_image(self):
        if hasattr(self, 'og_image'):
            return staticfiles_storage.url(self.og_image)

    def get_og_url(self):
        return self.request.build_absolute_uri(self.request.path)

    def get_og_site_name(self):
        return self.og_site_name

    def get_og_tags(self):
        tags = [
            {
                'property': 'locale',
                'content': self.get_og_locale()
            },
            {
                'property': 'type',
                'content': self.get_og_type()
            },
            {
                'property': 'title',
                'content': self.get_og_title()
            },
            {
                'property': 'description',
                'content': self.get_og_description()
            },
            {
                'property': 'url',
                'content': self.get_og_url()
            }
        ]

        image = self.get_og_image()
        if isinstance(image, File) and image:
            tags.extend(
                [
                    {
                        'property': 'image',
                        'content': image.url
                    }
                ]
            )
        elif isinstance(image, str) and image:
            tags.append(
                {
                    'property': 'image',
                    'content': image
                }
            )

        return tags

    def get_twitter_card(self):
        return self.twitter_card

    def get_twitter_title(self):
        return self.twitter_title or self.get_og_title()

    def get_twitter_description(self):
        return self.twitter_description or self.get_og_description()

    def get_twitter_site(self):
        return self.twitter_site

    def get_twitter_creator(self):
        return self.twitter_creator

    def get_twitter_tags(self):
        tags = [
            {
                'name': 'card',
                'content': self.get_twitter_card()
            },
            {
                'name': 'title',
                'content': self.get_twitter_title()
            },
            {
                'name': 'description',
                'content': self.get_twitter_description()
            },
            {
                'name': 'site',
                'content': self.get_twitter_site()
            },
            {
                'name': 'creator',
                'content': self.get_twitter_creator()
            }
        ]

        image = self.get_og_image()
        if isinstance(image, File) and image:
            tags.append(
                {
                    'name': 'image',
                    'content': image.url
                }
            )
        elif isinstance(image, str) and image:
            tags.append(
                {
                    'name': 'image',
                    'content': image
                }
            )

        return tags

    def get_context_data(self, **kwargs):
        return {
            'og_tags': self.get_og_tags(),
            'twitter_tags': self.get_twitter_tags(),
            **super().get_context_data(**kwargs)
        }


class OpenGraphArticleMixin(OpenGraphMixin):
    og_type = 'article'
    article_publisher = 'https://www.facebook.com/podiant'
    article_author = ''
    article_section = ''
    article_published_time = ''

    def get_article_publisher(self):
        return self.article_publisher

    def get_article_author(self):
        return self.article_author

    def get_article_section(self):
        return self.article_section

    def get_article_published_time(self):
        return self.article_published_time

    def get_article_tags(self):
        return [
            {
                'property': 'publisher',
                'content': self.get_article_publisher()
            },
            {
                'property': 'author',
                'content': self.get_article_author()
            },
            {
                'property': 'section',
                'content': self.get_article_section()
            },
            {
                'property': 'published_time',
                'content': self.get_article_published_time()
            }
        ]

    def get_context_data(self, **kwargs):
        return {
            'article_tags': self.get_article_tags(),
            **super().get_context_data(**kwargs)
        }


class LinkedDataMixin(object):
    ld_type = 'Thing'

    def get_ld_type(self):
        return self.ld_type

    def _load_ld_fixture(self, name):
        app, fixture = name.split('.')
        filename = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            app,
            'fixtures',
            'ld',
            '%s.json' % fixture
        )

        return self._prepare_fixture(filename)

    def _prepare_fixture(self, filename):
        with open(filename, 'rb') as f:
            data = json.load(f)

        for key, value in data.items():
            if isinstance(value, dict):
                import_name = value.pop('@import', None)
                if import_name:
                    import_fixture = self._load_ld_fixture(import_name)
                    data[key] = {
                        **import_fixture,
                        **value
                    }

        return data

    def get_ld_attributes(self):
        if hasattr(self, 'ld_attributes'):
            return self.ld_attributes

        if hasattr(self, 'ld_fixture'):
            return self._load_ld_fixture(self.ld_fixture)

        return {}

    def get_ld_url(self):
        if hasattr(self, 'ld_url'):
            return self.request.build_absolute_uri(
                reverse(self.ld_url)
            )

    def get_linked_data(self):
        data = {
            '@context': 'https://schema.org',
            '@type': self.get_ld_type(),
            **self.get_ld_attributes()
        }

        url = self.get_ld_url()
        if 'url' not in data and url:
            data['url'] = url

        return data

    def get_context_data(self, **kwargs):
        local = {}

        def get_json_ld():
            if 'ld' not in local:
                local['ld'] = mark_safe(
                    json.dumps(
                        kwargs.get('json_ld', self.get_linked_data()),
                        indent=4
                    )
                )

            return local['ld']

        return {
            'json_ld': get_json_ld,
            **super().get_context_data(**kwargs)
        }
