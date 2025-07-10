from django.test import TestCase


class LocalizationStatusListViewTest(TestCase):
    def test_url_accessible(self):
        response = self.client.get('/ressources/localization-status/list/')
        self.assertEqual(response.status_code, 200)
