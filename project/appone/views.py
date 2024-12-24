
import csv,json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render


class UploadCSVAPIView(APIView):
    renderer_classes = [JSONRenderer]  # Only allow JSON responses
    parser_classes = [MultiPartParser]  # typically used for file uploads
    
    def get(self, request, *args, **kwargs):
        return render(request, 'upload_csv.html')

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        # File extension validation
        if not file.name.endswith('.csv'):
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

            # Loop through the rows in the CSV file
            for index, row in enumerate(csv_file, start=1):
                # Normalize header by converting to lowercase and stripping extra spaces
                row = {key.strip().lower(): value for key, value in row.items()}
                print("Normalized row data:", row)  # Debugging line

                # Check for null values (empty fields for name, email, or age)
                if not row.get('name') or not row.get('email') or not row.get('age'):
                    rejected_records += 1
                    errors.append({"row": index, "errors": "Missing required fields (name, email, or age)."})
                    continue  # Skip this row

                # Check for duplicate email
                if row['email'] in email_set:
                    rejected_records += 1
                    errors.append({"row": index, "errors": f"Duplicate email entry: {row['email']}"})
                    continue  # Skip this row
                email_set.add(row['email'])

                # Validate with the serializer
                serializer = UserSerializer(data=row)
                if serializer.is_valid():
                    try:
                        serializer.save()
                        valid_records += 1
                    except Exception as save_error:
                        rejected_records += 1
                        errors.append({"row": index, "errors": str(save_error)})
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
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)