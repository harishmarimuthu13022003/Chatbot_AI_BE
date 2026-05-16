# AI Chat Application - Backend

This is the FastAPI backend for the AI Chat Application.

## Tech Stack
- **FastAPI**
- **MongoDB** (Motor Async Driver)
- **JWT Authentication** (Bcrypt)
- **Groq API Integration**

## Setup Instructions

1. Ensure **MongoDB** is running locally on the default port (`mongodb://localhost:27017`).
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root of the backend folder and add your Groq API keys:
   ```env
   MONGODB_URL="mongodb://localhost:27017"
   SECRET_KEY="your-secret-key-for-jwt"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=1440

   GROK_API_KEY_1="your_groq_api_key_here"
   GROK_API_KEY_2=""
   GROK_API_KEY_3=""
   GROK_API_KEY_4=""
   GROK_API_KEY_5=""
   ```
4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
