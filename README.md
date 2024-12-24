# csv-processor
This is a Django REST Framework (DRF) API endpoint that processes user data from a CSV file.

## Features
- **CSV File Upload**: Upload a CSV file via an API endpoint.
- **Data Validation**: The uploaded file is validated for required fields (name, email, and age) and duplicate email entries.
- **Error Handling**: Invalid rows with missing data or duplicate emails are logged with specific error messages.
- **Response Output**: The API returns a summary of the processed records, including valid and rejected entries.
- **JSON Result**: The result is saved to a `sample_output.json` file in the project root directory.

## Tech Stack
- **Django**: Python web framework for building the backend API.
- **Django REST Framework (DRF)**: Toolkit for building Web APIs in Django.
- **MySQL**: Default database (can be swapped with other databases like PostgreSQL).
- **Python 3.12**: The programming language for the backend.

## Installation

### Prerequisites
- Python 3.12
- Django
- Django REST Framework
- Git

### Step 1: Clone the repository
```bash
git clone https://github.com/Visakh2024/csv-processor.git
cd csv-processor
```

### Step 2: Set up a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply migrations
```bash
python manage.py migrate
```

### Step 5: Start the development server
```bash
python manage.py runserver
```

### Running Tests
```bash
python manage.py test
```







