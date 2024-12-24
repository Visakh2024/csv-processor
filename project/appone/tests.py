from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User

class UploadCSVAPITestCase(APITestCase):

    def test_upload_csv_valid_data(self):
        # Valid CSV with 2 records
        csv_content = "name,email,age\nJohn Doe,john@example.com,30\nJane Doe,jane@example.com,25"
        file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_valid_records'], 2)
        self.assertEqual(response.data['total_rejected_records'], 0)
        self.assertEqual(len(response.data['errors']), 0)

    def test_upload_csv_invalid_extension(self):
        # Invalid file extension (not .csv)
        file = SimpleUploadedFile("test.txt", b"Invalid content", content_type="text/plain")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Only .csv files are allowed.", response.data['error'])

    def test_upload_csv_with_missing_fields(self):
        # Invalid CSV with missing fields (age missing)
        csv_content = "name,email,age\nJohn Doe,john@example.com,\nJane Doe,jane@example.com,"
        file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_valid_records'], 0)
        self.assertEqual(response.data['total_rejected_records'], 2)
        self.assertEqual(len(response.data['errors']), 2)
        
    def test_upload_csv_with_duplicate_email(self):
        # CSV with duplicate email addresses
        csv_content = "name,email,age\nJohn Doe,john@example.com,30\nJane Doe,john@example.com,25"
        file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_valid_records'], 1)
        self.assertEqual(response.data['total_rejected_records'], 1)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertIn("Duplicate email entry: john@example.com", str(response.data['errors']))

    def test_upload_csv_with_invalid_data_type(self):
        # Invalid CSV with non-numeric age
        csv_content = "name,email,age\nJohn Doe,john@example.com,thirty\nJane Doe,jane@example.com,25"
        file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_valid_records'], 1)
        self.assertEqual(response.data['total_rejected_records'], 1)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertIn("A valid integer is required.", str(response.data['errors']))

    def test_upload_empty_csv(self):
        # Empty CSV file
        csv_content = ""
        file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The CSV file is empty.", response.data['error'])

    def test_upload_csv_with_extra_fields(self):
        # CSV with extra fields not in the model
        csv_content = "name,email,age,extra_field\nJohn Doe,john@example.com,30,extra_value\nJane Doe,jane@example.com,25,extra_value"
        file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_valid_records'], 2)
        self.assertEqual(response.data['total_rejected_records'], 0)
        self.assertEqual(len(response.data['errors']), 0)

