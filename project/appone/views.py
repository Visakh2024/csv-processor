import csv
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
import os
import re


class UploadCSVAPIView(APIView):
    renderer_classes = [JSONRenderer]  # Only allow JSON responses
    parser_classes = [MultiPartParser]  # Typically used for file uploads

    def get(self, request, *args, **kwargs):
        return render(request, 'upload_csv.html')

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        # File extension validation
        if not file or not file.name.endswith('.csv'):
            return Response({"error": "Only .csv files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the file is empty
        if file.size == 0:
            return Response({"error": "The CSV file is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Variables for tracking records
        valid_records = 0
        rejected_records = 0
        errors = []
        email_set = set()  # To track duplicate emails

        try:
            csv_file = csv.DictReader(file.read().decode('utf-8').splitlines())

            for index, row in enumerate(csv_file, start=1):
                # Normalize header and clean up row data
                row = {key.strip().lower(): value.strip() for key, value in row.items()}
                print("Normalized row data:", row)  # Debugging line

                row_errors = {}

                # Validate 'name' field
                if not row.get('name'):
                    row_errors['name'] = ["Name is required."]

                # Validate 'email' field
                email = row.get('email')
                if not email:
                    row_errors['email'] = ["Email is required."]
                elif not re.match(r'^\S+@\S+\.\S+$', email):
                    row_errors['email'] = ["Invalid email address."]
                elif email in email_set:
                    row_errors['email'] = [f"Duplicate email entry: {email}"]
                else:
                    email_set.add(email)

                # Validate 'age' field
                age = row.get('age')
                if not age:
                    row_errors['age'] = ["Age is required."]
                else:
                    try:
                        age = int(age)
                        if not (0 <= age <= 120):
                            row_errors['age'] = ["Age must be between 0 and 120."]
                    except ValueError:
                        row_errors['age'] = ["Age must be a valid integer."]

                # If there are field-specific errors, record them
                if row_errors:
                    rejected_records += 1
                    errors.append({"row": index, "errors": row_errors})
                    continue

                # Validate with the serializer
                serializer = UserSerializer(data=row)
                if serializer.is_valid():
                    try:
                        serializer.save()
                        valid_records += 1
                    except Exception as save_error:
                        rejected_records += 1
                        errors.append({"row": index, "errors": {"save_error": [str(save_error)]}})
                else:
                    rejected_records += 1
                    errors.append({"row": index, "errors": serializer.errors})

            # Prepare the result dictionary
            result = {
                "total_valid_records": valid_records,
                "total_rejected_records": rejected_records,
                "errors": errors,
            }

            # Save the result to a JSON file
            with open('sample_output.json', 'w') as json_file:
                json.dump(result, json_file, indent=4)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error occurred: {str(e)}")  # Debugging line
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
