from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import ProfileForm, ReportForm, ReportFileForm, PracticeForm
from ..models import Report, ReportFile, Profile

# python3 manage.py test MediGuard.tests.AnonymousUserTests

class AnonymousReportSubmissionTest(TestCase):
    def setUp(self):
        # Practice.objects.create(name="Test Practice", state="NY", city="New York", address="123 Test St", zipcode="10001")
        self.client = Client()

        # Setup for practice data
        self.practice_data = {
            'new_practice': 'Test Clinic',
            'state': 'CA',
            'city': 'Test City',
            'address': '123 Test St',
            'zipcode': '12345',
            'phone': '0123456789',
            'website': 'http://testclinic.com'
        }

        # Setup for report data
        self.report_data = {
            'subject': 'Anonymous Complaint',
            'description': 'Description of the complaint'
        }

        # URL for submitting the report
        self.url = reverse('MediGuard:report')

    def test_form_validation(self):
        incomplete_data = self.practice_data.copy()
        incomplete_data.update({'subject': '', 'description': 'Incomplete submission test'})
        response = self.client.post(self.url, incomplete_data)
        self.assertEqual(response.status_code, 200)
        report_form = response.context['report_form']
        self.assertTrue(report_form.is_bound)
        self.assertTrue(report_form.errors)
        self.assertIn('subject', report_form.errors)

    def test_form_invalid_data(self):
        url = reverse('MediGuard:report')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)


    def test_anonymous_report_submission(self):
        report_data = {
            'subject': 'Anonymous Complaint',
            'description': 'Description of the anonymous complaint',
        }

        practice_data = {
            'new_practice': 'Anonymous Practice',
            'state': 'CA',
            'city': 'Anon City',
            'address': '123 Anon St',
            'zipcode': '12345',
        }

        response = self.client.post(self.url, {**report_data, **practice_data})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Report.objects.filter(subject=report_data['subject']).exists())

    def test_report_and_file_submission(self):
        report_data = {
            'subject': 'Anonymous Complaint',
            'description': 'Description of the anonymous complaint',
        }

        practice_data = {
            'new_practice': 'Anonymous Practice',
            'state': 'CA',
            'city': 'Anon City',
            'address': '123 Anon St',
            'zipcode': '12345',
        }

        file = SimpleUploadedFile("testfile.txt", b"these are the file contents!")
        # Include file in the POST data
        form_data = {
            **report_data,
            **practice_data,
            'file': file,  # Field name should match the one in ReportFileForm
        }

        # Make a POST request with multipart encoding
        response = self.client.post(self.url, form_data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
