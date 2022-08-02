from django.views.generic import TemplateView
from replay.seo.mixins import SEOMixin, OpenGraphMixin, LinkedDataMixin
import os


class IndexView(SEOMixin, OpenGraphMixin, LinkedDataMixin, TemplateView):
    template_name = 'front/index.html'
    seo_title = 'Follow Podcast from Start'
    seo_description = (
        'Listen to a podcast from its original release date, then relive '
        'episodes at their original cadence.'
    )

    og_title = 'Replay'
    og_description = 'Follow a podcast from the beginning'
    og_image = 'images/og/index.png'
    canonical_url = 'index'
    ld_type = 'WebApplication'
    ld_url = 'index'
    ld_fixture = 'front.replay'


class AboutView(SEOMixin, TemplateView):
    template_name = 'front/about.html'
    seo_title = 'About Replay'

    def get_object(self):
        if not hasattr(self, 'object'):
            filename = os.path.join(
                os.path.dirname(__file__),
                'fixtures',
                'about.md'
            )

            title = 'About'
            lines = []

            with open(filename, 'r') as f:
                for line in f.read().splitlines():
                    if line and not any(lines) and line.startswith('# '):
                        title = line[2:].strip()
                        continue

                    lines.append(line)

            self.object = {
                'title': title,
                'body': '\n'.join(lines)
            }

        return self.object

    def get_context_data(self, **kwargs):
        return {
            'object': self.get_object(),
            **super().get_context_data(*kwargs)
        }
