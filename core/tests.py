from django.test import TestCase
from .models import SiteSetting, ContactMessage

class SiteSettingModelTest(TestCase):
    def test_create_setting(self):
        setting = SiteSetting.objects.create(key='site_name', value='ReWear')
        self.assertEqual(setting.key, 'site_name')
        self.assertEqual(setting.value, 'ReWear')

class ContactMessageModelTest(TestCase):
    def test_create_contact_message(self):
        msg = ContactMessage.objects.create(
            name='Alice',
            email='alice@example.com',
            subject='Test',
            message='Hello!'
        )
        self.assertEqual(msg.name, 'Alice')
        self.assertFalse(msg.is_read)
