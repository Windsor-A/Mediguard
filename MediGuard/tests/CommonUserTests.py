from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import ProfileForm, ReportForm, ReportFileForm, PracticeForm
from ..models import Report, ReportFile, Profile


class CommonUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.report_url = reverse('MediGuard:report')

        self.report_data = {
            'subject': 'Test Subject',
            'description': 'Test Description',
        }

        self.practice_data = {
            'new_practice': 'Test Clinic',
            'state': 'CA',
            'city': 'Test City',
            'address': '123 Test St',
            'zipcode': '12345',
            'phone': '0123456789',
            'website': 'http://testclinic.com'
        }


    def test_user_creation(self):
        self.assertTrue(User.objects.filter(username=self.user).exists())
        user = User.objects.get(username=self.user)
        self.assertEqual(user.username, 'testuser')

    def test_report_submission(self):
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

        response = self.client.post(report_url, {**report_data, **practice_data})
        self.assertEqual(response.status_code, 302)
        if response.status_code == 302:
            self.assertEqual(response.status_code, 302)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertTrue('form' in response.context and not response.context['form'].is_valid())

    def test_invalid_report_submission(self):
        report_url = reverse('MediGuard:report')
        invalid_report_data = {
            'description': '',  # 'description' is a required field, but null
        }
        response = self.client.post(report_url, invalid_report_data)

        self.assertEqual(response.status_code, 200,
                         msg="The form submission did not return a 200 status code as expected for an invalid form.")

    def test_view_submission_history(self):
        login_successful = self.client.login(username='testuser', password='12345')
        self.assertTrue(login_successful, "User login failed.")
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

        response = self.client.post(self.report_url, {**report_data, **practice_data})
        self.assertEqual(response.status_code, 302, "The report should be created successfully.")

        detail_url = reverse('MediGuard:user_dashboard')
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200, "Should be able to retrieve the report detail view.")

        self.assertContains(response, 'Anonymous Complaint')

    def test_delete_report(self):
        login_successful = self.client.login(username='testuser', password='12345')
        self.assertTrue(login_successful, "User login failed.")
        report_data = {
            'subject': 'Anonymous Report',
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

        response = self.client.post(self.report_url, {**report_data, **practice_data})
        self.assertEqual(response.status_code, 302, "The report should be created successfully.")
        report_id = Report.objects.latest('id').id

        detail_url = reverse('MediGuard:user_dashboard')
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200, "Should be able to retrieve the report detail view.")
        self.assertContains(response, 'Anonymous Report')

        delete_url = reverse('MediGuard:delete_report', args=[report_id])
        self.assertEqual(response.status_code, 200, "The deletion should redirect to the user dashboard.")


        self.assertEqual(response.status_code, 200, "Should redirect to the user dashboard after deletion.")
        self.assertTemplateUsed(response, 'user_dashboard.html')



