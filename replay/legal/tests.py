from django.test import TestCase


class TermsViewTests(TestCase):
    def test(self):
        response = self.client.get('/terms/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'legal/document.html',
            [t.name for t in response.templates]
        )


class PrivacyViewTests(TestCase):
    def test(self):
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'legal/document.html',
            [t.name for t in response.templates]
        )
