

# # Create your tests here.

        
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadCSVAPITestCase(APITestCase):

    def test_upload_csv_valid_data(self):
        # Valid CSV with 2 records
        csv_content = "name,email,age\nJohn Doe,john@example.com,30\nJane Doe,jane@example.com,25"
        file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_valid_records'], 2)

    def test_upload_csv_invalid_extension(self):
        # Invalid file extension (not .csv)
        file = SimpleUploadedFile("test.txt", b"Invalid content", content_type="text/plain")
        response = self.client.post('/api/upload-csv/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Only .csv files are allowed.", response.data['error'])
        