# Career Forge: MVP Development

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.92.0-green?logo=fastapi)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_1.5_Pro-purple?logo=google&logoColor=white)

Career Forge is an AI-powered platform that turns resume analysis into a gamified career journey. It uses a Large Language Model (LLM) to create detailed user profiles, break down skills, and generate personalized quests for growth.

## ✨ Features

- **Resume Analysis**: Uses Google Gemini 1.5 Pro to extract skills, experience, and context, then generates a human-like summary.  
- **Gamified Dashboard**: Builds a profile with Rank (E–S) and Level (1–99), plus a radar chart of strengths.  
- **Quest System**: Acts as a “Quest Master,” creating tailored challenges and learning goals.  
- **Modern UI**: Dark-themed interface with HTML, CSS, and Chart.js for visualization.  

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn  
- **AI/NLP**: Google Gemini 1.5 Flash, spaCy  
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js  
- **Data Handling**: Pydantic, python-dotenv  
- **File Parsing**: pypdf, python-docx  

## 🚀 Getting Started

Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Environment Setup

Create a `.env` file in the project root:

```
GOOGLE_API_KEY="your-real-api-key-here"
```

The `.gitignore` is already set up to exclude it.

### Run the Server

Start the backend with Uvicorn:

```bash
uvicorn career_forge.api.main:app --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## ⚙️ API

**`POST /api/v1/hackrx/run`**  
- **Body**: `multipart/form-data`  
- **Field**: `file` (resume file, .pdf or .docx)  

---
