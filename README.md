# AI Job Hunter

AI-powered job automation platform for cybersecurity roles. Scrapes job boards, ranks listings against your resume, generates Excel reports, and emails them on a schedule.

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLite
- **Scraping:** Playwright, BeautifulSoup
- **AI:** Gemini API (preferred) or OpenAI
- **Reports:** Pandas, OpenPyXL
- **Frontend:** Next.js 15, TailwindCSS (Phase 7)

## Quick Start

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate (Windows)
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env

# 5. Run the API
uvicorn backend.app:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

## Project Structure

```
backend/
    app.py          # FastAPI entry point
    config.py       # Environment settings
    api/            # HTTP route handlers
    services/       # Business logic
    models/         # Data models
    scraper/        # Job collection
    ai/             # Resume matching
    database/       # Persistence layer
    email/          # Report delivery
    excel/          # Report generation
    utils/          # Shared helpers
```

## Development Phases

| Phase | Feature              | Status |
|-------|----------------------|--------|
| 1     | Project setup        | ✅     |
| 2     | Job collection       |        |
| 3     | Database storage     |        |
| 4     | AI resume matching   |        |
| 5     | Excel generation     |        |
| 6     | Email automation     |        |
| 7     | Next.js dashboard    |        |
| 8     | Authentication       |        |
| 9     | Scheduler            |        |
| 10    | Deployment           |        |

## License

Private — for personal use.
