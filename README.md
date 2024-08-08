
# Health App Django Project

## Overview
This project is a Django-based application designed to manage and analyze health-related data, such as sleep patterns and step counts. The app offers various APIs for extracting insights from user data, integrating AI-powered responses using the OpenAI API.

## Features
- **User Management:** Create, manage, and authenticate users.
- **Health Data Management:** Track user health metrics including sleep, steps, and more.
- **APIs:** RESTful APIs for retrieving health insights.
- **AI Integration:** Generate personalized health advice using the OpenAI API.

## Prerequisites
- **Python 3.x**
- **Django 3.x or later**
- **pip** (Python package installer)
- **SQLite** 
- **OpenAI API Key** ([Sign up here](https://beta.openai.com/signup/))

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Update the `views.py` file in the `health_app` folder. On line 138, replace the placeholder with your actual OpenAI API key:

```python
api_key = 'your_openai_api_key_here'
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Server
```bash
python manage.py runserver
```

## Usage

### Generating Dummy Health Data
You can generate dummy data for testing purposes using the following command:
```bash
python manage.py generate_data
```

### API Endpoints

- **`/api/step-comparison/`**: 
  - **Description**: Retrieves user's sleep condition, step 1 condition, and step 2 condition without an OpenAI response.
  - **Method**: GET
  - **Response**: User's sleep condition, step 1 condition, and step 2 condition.

- **`/api/ai-result/`**: 
  - **Description**: Retrieves user's sleep condition, step 1 condition, and step 2 condition and generates an AI response.
  - **Method**: GET
  - **Response**: User's sleep condition, step 1 condition, step 2 condition, and AI-generated response.


