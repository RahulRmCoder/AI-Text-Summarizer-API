# AI Text Summarizer API (Django + Django REST Framework + Groq API)

## 📌 Project Overview

This project is an **AI-powered text summarizer and rewriter API** built using **Django** and **Django REST Framework (DRF)**. It integrates with the **Groq API** to process and generate text-based responses.

## 🚀 Technologies Used

- **Python** (Programming Language)
- **Django** (Backend Framework)
- **Django REST Framework** (API Development)
- **Groq API** (AI Model for Summarization & Rewriting)
- **Postman / cURL** (API Testing)
- **dotenv** (Environment Variable Management)
- **requests** (HTTP Requests to External API)

---

## ✅ Step 1: Setup Django Project & Install Dependencies

### 1️⃣ Install Python & Virtual Environment

Make sure you have **Python 3.8+** installed. If not, install it from [Python.org](https://www.python.org/downloads/).

Create and activate a virtual environment:

```sh
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2️⃣ Install Django & Required Libraries

```sh
pip install django djangorestframework requests python-dotenv
```

### 3️⃣ Create a New Django Project

```sh
django-admin startproject ai_summarizer
cd ai_summarizer
```

### 4️⃣ Create a New Django App

```sh
python manage.py startapp summarizer
```

### 5️⃣ Add App to `settings.py`

Edit `ai_summarizer/settings.py` and add the following:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'summarizer',  # Custom App
]
```

### 6️⃣ Configure `.env` File

Create a `.env` file in the **root** of your project and add your **Groq API Key**:

```env
GROQ_API_KEY=your_api_key_here
```

Then, install `python-dotenv` to read `.env` variables:

```sh
pip install python-dotenv
```

Update `ai_summarizer/settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

---

## ✅ Step 2: Setup API Integration (Groq API)

### 1️⃣ Create `services.py` to Call Groq API

Create a new file: `summarizer/services.py` and add:

```python
import os
import requests

groq_api_url = "https://api.groq.com/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_text(input_text):
    if not GROQ_API_KEY:
        return {"error": "Missing API Key. Check .env file."}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": input_text}],
        "temperature": 0.7
    }

    try:
        response = requests.post(groq_api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
```

---

## ✅ Step 3: Create Django REST API Endpoints

### 1️⃣ Define Serializers (`summarizer/serializers.py`)

```python
from rest_framework import serializers

class SummarizeSerializer(serializers.Serializer):
    text = serializers.CharField()

class RewriteSerializer(serializers.Serializer):
    text = serializers.CharField()
    style = serializers.CharField()
```

### 2️⃣ Create API Views (`summarizer/views.py`)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SummarizeSerializer, RewriteSerializer
from .services import summarize_text

class SummarizeView(APIView):
    def post(self, request):
        serializer = SummarizeSerializer(data=request.data)
        if serializer.is_valid():
            result = summarize_text(serializer.validated_data['text'])
            return Response({"summary": result}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RewriteView(APIView):
    def post(self, request):
        serializer = RewriteSerializer(data=request.data)
        if serializer.is_valid():
            result = summarize_text(serializer.validated_data['text'])  # Placeholder
            return Response({"rewritten_text": result}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 3️⃣ Define URLs (`summarizer/urls.py`)

```python
from django.urls import path
from .views import SummarizeView, RewriteView

urlpatterns = [
    path('summarize/', SummarizeView.as_view(), name='summarize'),
    path('rewrite/', RewriteView.as_view(), name='rewrite'),
]
```

### 4️⃣ Register URLs in Main `urls.py`

Edit `ai_summarizer/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('summarizer.urls')),
]
```

---

## ✅ Running the Server

```sh
python manage.py runserver
```

---

## ✅ Testing with cURL & Postman

### Summarization API Test (cURL)

```sh
curl -X POST http://127.0.0.1:8000/api/summarize/ \
     -H "Content-Type: application/json" \
     -d '{"text": "Artificial Intelligence is transforming the world with automation."}'
```

### Rewriting API Test (cURL)

```sh
curl -X POST http://127.0.0.1:8000/api/rewrite/ \
     -H "Content-Type: application/json" \
     -d '{"text": "AI is changing the world", "style": "casual"}'
```

### Test in Postman

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/api/summarize/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**

```json
{
    "text": "Artificial Intelligence is transforming the world with automation."
}
```

---

## 🎯 Next Steps

- ✅ Implement frontend UI
- ✅ Add authentication & user history
- ✅ Improve AI model selection

---

## 📌 Author

Rahul Rajasekharan Menon

