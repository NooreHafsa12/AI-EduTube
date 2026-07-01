# 🎓 AI-EduTube

> **AI-powered YouTube Study Assistant that transforms educational videos into AI summaries, interactive flashcards, quizzes, and downloadable PDF notes through a modern SaaS-inspired interface.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![HTML](https://img.shields.io/badge/HTML-5-orange)
![CSS](https://img.shields.io/badge/CSS-3-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

AI-EduTube is an intelligent learning platform that converts YouTube educational videos into structured study material.

Simply paste a YouTube video URL and AI-EduTube automatically generates:

- 📝 Smart AI Summary
- 🧠 Interactive Flashcards
- ❓ Quiz
- 📄 Downloadable PDF Notes

Designed with a modern pastel SaaS interface, AI-EduTube helps students revise faster and learn more effectively.

---

# ✨ Features

### 🎥 YouTube Video Analysis

- Paste YouTube URL
- Automatic transcript extraction
- Video title
- Channel name
- Duration
- Thumbnail preview

---

### 📝 AI Summary

- Bullet point summary
- Easy-to-read notes
- Clean formatting
- Copy summary

---

### 🧠 Interactive Flashcards

- AI-generated flashcards
- Flip animation
- Previous / Next navigation
- Progress counter

---

### ❓ Smart Quiz

- Multiple-choice questions
- Instant answer validation
- Progress bar
- Final score screen
- Retry quiz

---

### 📄 PDF Export

Generate beautiful study notes containing:

- Video Information
- AI Summary
- Flashcards
- Quiz Questions
- Correct Answers

---

### 💾 Session Cache

The application stores:

- Transcript
- Summary
- Flashcards
- Quiz

Users only need to paste the YouTube URL once.

---

### 🎨 Modern UI

- Glassmorphism
- Pastel gradients
- Responsive layout
- Light / Dark mode
- Smooth animations
- SaaS-inspired design

---

# 🛠️ Tech Stack

## Backend

- Python
- Flask

## Frontend

- HTML5
- CSS3
- JavaScript (ES6)

## Libraries

- youtube-transcript-api
- yt-dlp
- FPDF
- python-dotenv

---

# 📂 Project Structure

```text
AI-EduTube/
│
├── app.py
├── config.py
├── requirements.txt
│
├── services/
│   ├── transcript_service.py
│   ├── youtube_service.py
│   ├── summary_service.py
│   ├── flashcard_service.py
│   ├── quiz_service.py
│   ├── pdf_service.py
│   └── cache_service.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── components/
│   ├── dashboard.html
│   └── index.html
│
└── generated/
```

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/NooreHafsa12/AI-EduTube.git
```

Go to project folder

```bash
cd AI-EduTube
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python app.py
```

Open

```text
http://127.0.0.1:5000
```

---

# 📸 Screenshots

## Landing Page

_Add screenshot here_

## Dashboard

_Add screenshot here_

## AI Summary

_Add screenshot here_

## Flashcards

_Add screenshot here_

## Quiz

_Add screenshot here_

## PDF Export

_Add screenshot here_

---

# 🎯 Future Enhancements

- 🤖 AI Mentor Chat
- 🧠 Mind Map Generator
- 📊 Learning Analytics
- ☁️ Cloud Database
- 📱 Mobile App
- 🌍 Multi-language Support
- 📚 Study History
- 🔖 Bookmark Videos
- 🎤 Voice Interaction
- 📈 Progress Tracking

---

# 👩‍💻 Author

**Shaik Noore Hafsa**

- 🎓 B.Tech Computer Science Engineering
- 💻 Python | Flask | AI | Web Development
- 🌐 GitHub: https://github.com/NooreHafsa12

---

# ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future improvements.
