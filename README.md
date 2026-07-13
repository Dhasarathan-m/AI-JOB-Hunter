# AI Job Hunter

An AI-powered full-stack job aggregation platform that automatically discovers cybersecurity jobs, stores them in a database, and presents them through a modern web interface.

## Features

- Automated job scraping from multiple job sources
- FastAPI REST API
- Next.js dashboard
- Job search and filtering
- Resume upload
- SQLite database
- Interactive Swagger API documentation
- Modular scraping pipeline
- Automated testing

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLite
- Playwright
- BeautifulSoup

### Frontend
- Next.js 15
- React
- Tailwind CSS

### Tools
- Git
- GitHub
- Uvicorn

---

## Project Structure

```text
backend/
frontend/
tests/
docs/
data/
```

---

## Getting Started

### Clone

```bash
git clone https://github.com/Dhasarathan-m/AI-JOB-Hunter.git
```

### Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Configure

```bash
copy .env.example .env
```

### Run Backend

```bash
uvicorn backend.app:app --reload
```

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## API Documentation

After starting the backend:

```
http://127.0.0.1:8000/docs
```

---

## Screenshots

> Add screenshots here after deployment.

- Home page
- Job listing page
- Job details page
- Swagger API
- Resume upload

---

## Future Improvements

- User authentication
- Email notifications
- AI-powered resume scoring
- Job recommendations
- Docker support
- CI/CD pipeline

---

## Author

**Dhasa Rathan**

GitHub:
https://github.com/Dhasarathan-m