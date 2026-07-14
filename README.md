# 🌿 Banjara Cultural Knowledge Platform

> AI-Powered Cultural Knowledge Platform for the Banjara Community

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

## 📖 About

This is a full-stack web application that digitally preserves and
promotes the rich cultural heritage of the Banjara (Lambani) community
of India using Artificial Intelligence and modern web technology.

## ✨ Features

- 🌐 Bilingual platform — English & ಕನ್ನಡ (Kannada)
- 🤖 AI-powered smart search (30+ Banjara topics)
- 🛕 9 sacred temple profiles with Google Maps
- 🎭 8-section culture guide (history, dress, marriage, festivals...)
- 🌿 Karnataka Lambani — 16 district coverage
- 📝 Cultural quiz with 25 questions (5 categories)
- 🖼️ Gallery — Photos, Songs, Videos, YouTube
- 🔑 User registration and login system
- 🛡️ Admin panel — content, media, users management
- 📱 Mobile responsive design

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask |
| Database | MySQL 8.0 |
| Frontend | HTML5, CSS3, JavaScript |
| AI/NLP | Python keyword NLP |
| Auth | SHA-256 hashing |

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/santoshpl2005/banjara-platform.git
cd banjara-platform
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Create local config

Copy `config_example.py` to `config.py` and update your MySQL credentials.
You can also use `.env.example` for local environment variables.

### 4. Initialize the database

Import `database_setup.sql` into your MySQL server.

### 5. Run locally

```bash
python app.py
```

## 🚢 Deploy to Railway

1. Push this repository to GitHub.
2. In Railway, create a new project and connect the GitHub repo.
3. Add a MySQL plugin or external MySQL database, then configure these environment variables:
   - `SECRET_KEY`
   - `MYSQL_HOST`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
   - `MYSQL_DB`
   - `UPLOAD_FOLDER` (optional, default: `static/images`)
4. Railway uses the root `Procfile` already included in this repo:

```text
web: gunicorn -b 0.0.0.0:$PORT app:app
```

5. Ensure Railway installs dependencies from `requirements.txt`.
6. Use the Railway MySQL connection info to populate the MySQL environment variables.
7. If you need file uploads in production, consider using a cloud storage solution because the app currently stores uploads in local `static/`.
8. Deploy and monitor logs from the Railway dashboard.

> Note: `config.py` is already set up to read MySQL and secret values from environment variables, which works cleanly on Railway.
