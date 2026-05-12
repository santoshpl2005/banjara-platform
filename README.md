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
git clone https://github.com/yourusername/banjara-platform.git
cd banjara-platform
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup database
- Install MySQL
- Create database: `banjara_db`
- Run the SQL from `database_setup.sql`

### 5. Configure settings
```bash
copy config_example.py config.py
# Edit config.py with your MySQL password
```

### 6. Run the application
```bash
python app.py
```

Open browser: **http://127.0.0.1:5000**

## 🔐 Admin Panel

URL: `http://127.0.0.1:5000/admin`
- Username: `admin`
- Password: `admin123`

## 📱 Mobile Access

Run the app and open on phone:
`http://YOUR_COMPUTER_IP:5000`

## 🗄️ Database Tables

- `users` — User accounts
- `admins` — Admin login
- `cultural_content` — Culture articles
- `temples` — Temple information
- `media` — Images, audio, video
- `user_queries` — AI chat log
- `quiz_questions` — Quiz questions
- `password_resets` — Password reset tokens

## 📋 Project Information

- **Community:** Banjara (Lambani) of India
- **Language:** English + Kannada (ಕನ್ನಡ)
- **Duration:** 2 Months
- **Type:** Full-Stack Web Application

## 🙏 Jai Sevalal!

*Preserving Banjara Heritage Through Technology*