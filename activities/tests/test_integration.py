from datetime import datetime
from django.urls import reverse
from django.utils.timezone import make_aware, get_current_timezone
from activities.models import Activity
from django.test import TestCase
from pets.models import Pet
from django.contrib.auth import get_user_model

class TestActivityReportView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')  # Log in the user
        self.pet = Pet.objects.create(name='Test Pet', user=self.user, age=1, weight=10)

    def test_activity_report_view(self):
        url = reverse('activity_report', args=[self.pet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activity_report.html')

    def test_activity_report_view_with_activities(self):
        # Create multiple activities for the pet
        Activity.objects.create(
            pet=self.pet,
            user=self.user,
            activity_name='Activity 2',
            date_completed=make_aware(datetime(2022, 1, 2), get_current_timezone())
        )
        Activity.objects.create(
            pet=self.pet,
            user=self.user,
            activity_name='Activity 3',
            date_completed=make_aware(datetime(2022, 1, 3), get_current_timezone())
        )

        url = reverse('activity_report', args=[self.pet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activity_report.html')
        self.assertEqual(len(response.context['activities']), 2)

    def test_activity_report_view_with_filters(self):
        # Create multiple activities for the pet
        Activity.objects.create(
            pet=self.pet,
            user=self.user,
            activity_name='Activity 2',
            date_completed=make_aware(datetime(2022, 1, 2), get_current_timezone())
        )
        Activity.objects.create(
            pet=self.pet,
            user=self.user,
            activity_name='Activity 3',
            date_completed=make_aware(datetime(2022, 1, 3), get_current_timezone())
        )

        url = reverse('activity_report', args=[self.pet.id])
        response = self.client.get(url, {'start_date': '2022-01-02'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activity_report.html')
        self.assertEqual(len(response.context['activities']), 2)

    def test_activity_report_view_with_invalid_filters(self):
        url = reverse('activity_report', args=[self.pet.id])
        response = self.client.get(url, {'invalid_filter': 'invalid_value'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activity_report.html')
        self.assertEqual(len(response.context['activities']), 0)

    def test_activity_report_view_with_no_pet(self):
        url = reverse('activity_report', args=[9999])  # Invalid pet ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_activity_report_view_with_no_activities(self):
        # Delete all activities for the pet
        Activity.objects.all().delete()

        url = reverse('activity_report', args=[self.pet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activity_report.html')
        self.assertEqual(len(response.context['activities']), 0)