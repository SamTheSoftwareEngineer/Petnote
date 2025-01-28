from django.test import SimpleTestCase
from django.urls import reverse

class ActivityUrlsTest(SimpleTestCase):
    def test_activity_report_url(self):
        url = reverse('activity_report', kwargs={'pet_id': 1})
        self.assertEqual(url, '/activities/1/report/')
    
    def test_add_activity_url(self):
        url = reverse('add_activity', kwargs={'pet_id': 1})
        self.assertEqual(url, '/activities/1/add/')
    
    def test_edit_activity_url(self):
        url = reverse('edit_activity', kwargs={'pk': 1})
        self.assertEqual(url, '/activities/edit/1/')
    
    def test_delete_activity_url(self):
        url = reverse('delete_activity', kwargs={'activity_id': 1})
        self.assertEqual(url, '/activities/delete/1/')
    
