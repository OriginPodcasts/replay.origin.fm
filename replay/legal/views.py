from django.urls import reverse
from django.views.generic import TemplateView
from replay.seo.mixins import SEOMixin
import os


class LegalView(SEOMixin, TemplateView):
    def get_object(self):
        if not hasattr(self, 'object'):
            filename = os.path.join(
                os.path.dirname(__file__),
                'fixtures',
                '%s.md' % self.document_name
            )

            title = self.document_name.replace('_', ' ').capitalize()
            lines = []
            updated = None

            with open(filename, 'r') as f:
                for line in f.read().splitlines():
                    if line and not any(lines) and line.startswith('# '):
                        title = line[2:].strip()
                        continue

                    if line and line.startswith('Last updated '):
                        updated = line[13:].strip()
                        continue

                    lines.append(line)

            self.object = {
                'title': title,
                'updated': updated,
                'body': '\n'.join(lines)
            }

        return self.object

    def get_template_names(self):
        return (
            'legal/%s.html' % self.document_name,
            'legal/document.html'
        )

    def get_seo_title(self):
        obj = self.get_object()
        return obj['title']

    def get_canonical_url(self):
        return self.request.build_absolute_uri(
            reverse(self.document_name)
        )

    def get_context_data(self, **kwargs):
        return {
            'object': self.get_object(),
            **super().get_context_data(*kwargs)
        }


class PrivacyView(LegalView):
    document_name = 'privacy'


class CookiesView(LegalView):
    document_name = 'cookies'
