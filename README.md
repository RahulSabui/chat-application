# Python App

A Django-based web application with authentication, chat, and conversation features.

## Features
- Django REST Framework APIs
- JWT authentication
- User accounts and permissions
- Chat and conversation modules
- Redis-backed channel support

## Tech Stack
- Python
- Django
- Django REST Framework
- channels / channels-redis
- MySQL

## Local Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the required settings, for example:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure
- `accounts/` – user accounts and authentication logic
- `chat/` – chat-related models, serializers, and services
- `conversations/` – conversation support
- `config/` – Django settings and URL configuration

## Notes
- Make sure Redis is available if you want to use the real-time chat features.
- The project uses environment variables from `.env` for configuration.
