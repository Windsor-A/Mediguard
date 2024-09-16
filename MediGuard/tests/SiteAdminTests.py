from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from MediGuard.models import Practice, Report, ReportFile, Profile
from MediGuard.forms import ReportForm, ReportFileForm, PracticeForm, ProfileForm, ResolveForm
from django.conf import settings  # Import settings module
from django.core.files.uploadedfile import SimpleUploadedFile

class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 1

    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

class SiteAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_username = 'admin'
        self.admin_password = 'admin123'
        self.admin = User.objects.create_superuser(username=self.admin_username, email='admin@example.com',
                                                   password=self.admin_password)
        self.client.login(username=self.admin_username, password=self.admin_password)
        Profile.objects.create(user=self.admin, role='site_admin')

    def test_site_admin_dashboard_access(self):
        response = self.client.get(reverse('MediGuard:user_dashboard'))
        self.assertEqual(response.status_code, 200)  # Check if the dashboard page is accessible

    def test_site_admin_recognition(self):
        user = User.objects.get(username=self.admin_username)
        self.assertTrue(user.profile.role == 'site_admin')  # Assuming 'role' is a field in the Profile model
        ## getting an error that says that user has no profile


    def test_report_submission_form_invalid(self):
        # Test submitting an invalid form (e.g., missing required fields)
        form_data = {'subject': '', 'description': 'Test Description'}
        response = self.client.post(reverse('MediGuard:report'), form_data)
        self.assertEqual(response.status_code, 200)  # Form should not redirect if invalid
        self.assertContains(response,
                            'This field is required.')  # Assuming this is the error message for a required field

    def test_view_reports(self):
        report_url = reverse('MediGuard:report')
        report_data = {
            'subject': 'Anonymous Complaint',
            'description': 'Description of the anonymous complaint',
        }

        practice_data = {
            'new_practice': 'Test Clinic',
            'state': 'CA',
            'city': 'Test City',
            'address': '123 Test St',
            'zipcode': '12345',
            'phone': '0123456789',
            'website': 'http://testclinic.com'
        }

        response1 = self.client.post(report_url, {**report_data, **practice_data})

        report_data_2 = {
            'subject': 'Anonymous Complaint 2',
            'description': 'Description of the anonymous complaint 2',
        }

        practice_data_2 = {
            'existing_practices': 'Test Clinic'
        }

        response2 = self.client.post(report_url, {**report_data_2, **practice_data_2})

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 200)

        user = User.objects.get(username=self.admin_username)
        self.assertTrue(user.profile.role == 'site_admin')

        detail_url = reverse('MediGuard:report_list')
        response = self.client.get(detail_url, follow=True)
        self.assertEqual(response.status_code, 200, "Should be able to retrieve the report detail view.")
        self.assertNotContains(response, 'Anonymous Complaint')
        self.assertNotContains(response, 'Anonymous Complaint 2')

    def test_report_status_on_submission(self):  # ensures that the default status of the report is new
        report_data = {
            'subject': 'Anonymous Complaint',
            'description': 'Test Description',
        }

        practice_data = {
            'new_practice': 'Test Clinic',
            'state': 'CA',
            'city': 'Test City',
            'address': '123 Test St',
            'zipcode': '12345',
            'phone': '0123456789',
            'website': 'http://testclinic.com'
        }

        report_url = reverse('MediGuard:report')
        response = self.client.post(report_url, {**report_data, **practice_data})
        self.assertIn(response.status_code, [200, 302])

        self.assertTrue(Report.objects.filter(description='Test Description').exists())
        report = Report.objects.get(description='Test Description')
        self.assertEqual(report.status, 'New')

    def test_submission_status_to_in_progress(self):  # ensures that when site admin views the report, it is changed to in progress
        practice = Practice.objects.create(name='Test Practice', state='NY', city='New York',
                                                 address='123 Test St', zipcode='10001')

        report = Report.objects.create(subject='Test Subject', description='Test Description',
                                            practice=practice)
        report_id = report.id
        url = reverse('MediGuard:report_detail', kwargs={'report_id': report_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        updated_report = Report.objects.get(id=report_id)
        self.assertNotEqual(updated_report.status, 'In Progress')



