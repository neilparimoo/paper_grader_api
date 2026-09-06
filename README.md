# 📝 Paper Grader API

An automated GCSE exam paper grading API built with **FastAPI** and powered by **Google Gemini GenAI**. Upload completed exam papers (PDF or images), specify the exam board, subject, tier, and year, and receive automated marks, percentage scores, estimated GCSE grades, and concise feedback based on official mark schemes.

---

## ✨ Features

- **Automated AI Grading:** Leverages Google's `gemini-3.6-flash` model with multimodal file ingestion to evaluate student answers against mark schemes.
- **Board & Subject Validation:** Built-in validation against official GCSE exam board specifications.
- **FastAPI Backend:** High-performance REST API with auto-generated Swagger UI and ReDoc interactive documentation.
- **Concise Feedback:** Returns a targeted summary containing total marks awarded, percentage, estimated grade, and diagnostic feedback.

---

## 🛠 Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Server:** [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- **AI / LLM:** [Google GenAI SDK](https://github.com/google/generative-ai-python) (`google-genai`, `gemini-3.6-flash`)
- **Package Manager:** [uv](https://docs.astral.sh/uv/) / `pip`
- **Runtime:** Python 3.13+

---

## 📂 Project Structure

```text
paper_grader_api/
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore rules (.env, .venv, cache, etc.)
├── gcse_boards_config.py  # GCSE board & subject mapping configuration
├── main.py                # FastAPI app initialization and route definitions
├── paper.py               # Paper class, validation logic, and Gemini grading pipeline
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Locked dependency versions
└── README.md              # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+** installed on your system.
- A **Google Gemini API Key** (obtainable from [Google AI Studio](https://aistudio.google.com/)).
- Recommended: [uv](https://docs.astral.sh/uv/) package manager for fast, reproducible dependency management.

### Installation

#### Option 1: Using `uv` (Recommended)

1. Clone or navigate to the project directory:
   ```bash
   cd paper_grader_api
   ```

2. Sync and install dependencies into a virtual environment:
   ```bash
   uv sync
   ```

#### Option 2: Using standard `pip` and `venv`

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn google-genai python-multipart python-dotenv
   ```

---

## ⚙️ Configuration & API Key

The application communicates with Google Gemini via the `google-genai` SDK and loads environment variables using `python-dotenv`.

1. Copy the sample environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY="your-gemini-api-key-here"
   ```

Alternatively, you can export it directly in your shell session:
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

In [paper.py](file:///Users/neilparimoo/PycharmProjects/paper_grader_api/paper.py), the key is loaded automatically:
```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
```

---

## 🏃 Running the Application

Start the local development server with auto-reload enabled:

### Using `uv`:
```bash
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Using standard `uvicorn`:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

### Interactive API Documentation
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Reference

### `POST /grade-paper`

Upload an exam paper and receive automated grading results.

#### Request Parameters (`multipart/form-data`)

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `file` | `UploadFile` (binary) | **Yes** | — | Completed exam paper (PDF or image). |
| `board` | `string` | No | `"aqa"` | Exam board (`aqa`, `edexcel`, `ocr`, `eduqas`). |
| `subject` | `string` | No | `"maths"` | GCSE subject (must match the board's offerings). |
| `tier` | `string` | No | `"Higher"` | Exam tier (e.g. `Higher`, `Foundation`). |
| `year` | `integer` | No | `2025` | Exam session year (between `2000` and `2026`). |

#### Example Request (`curl`)

```bash
curl -X POST "http://127.0.0.1:8000/grade-paper" \
  -F "file=@sample_exam.pdf" \
  -F "board=aqa" \
  -F "subject=maths" \
  -F "tier=Higher" \
  -F "year=2025"
```

#### Example Request (Python)

```python
import requests

url = "http://127.0.0.1:8000/grade-paper"

files = {"file": ("exam.pdf", open("sample_exam.pdf", "rb"), "application/pdf")}
data = {
    "board": "aqa",
    "subject": "maths",
    "tier": "Higher",
    "year": 2025
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

#### Success Response (`200 OK`)

```json
{
  "message": "Grading Complete!",
  "feedback": "Total Marks: 68/80 (85%). Estimated Grade: 8. Strong working shown on calculus and algebraic fractions. Lost minor marks on question 14 due to missing units in the final step. Great overall structure and logical clarity."
}
```

#### Error Response (`400 Bad Request`)

If an invalid board, subject, or year is supplied:

```json
{
  "detail": "subject must be one of these ['english', 'maths', 'biology', ...]"
}
```

---

## 📋 Supported Exam Boards & Subjects

Supported boards configured in [gcse_boards_config.py](file:///Users/neilparimoo/PycharmProjects/paper_grader_api/gcse_boards_config.py):

| Board | Sample Supported Subjects |
| :--- | :--- |
| **AQA** (`aqa`) | `english`, `maths`, `biology`, `chemistry`, `physics`, `history`, `geography`, `computer_science`, `french`, `spanish`, `business`, `psychology`, ... |
| **Edexcel** (`edexcel`) | `english`, `maths`, `biology`, `chemistry`, `physics`, `history`, `geography`, `computer_science`, `business`, `dt`, `music`, ... |
| **OCR** (`ocr`) | `english`, `maths`, `biology`, `chemistry`, `physics`, `history`, `latin`, `computer_science`, `foodtech`, `economics`, ... |
| **Eduqas** (`eduqas`) | `english`, `maths`, `history`, `geography`, `religious`, `sociology`, `latin`, `media`, `business`, ... |

*(See [gcse_boards_config.py](file:///Users/neilparimoo/PycharmProjects/paper_grader_api/gcse_boards_config.py) for the complete list for each board).*

---

## 🔮 Planned Enhancements

- [ ] Support asynchronous Gemini API calls (`client.aio`) for non-blocking execution.
- [ ] Temporary file cleanup after upload to Google GenAI.
- [ ] Structured JSON grading output (e.g. per-question mark breakdowns).
- [ ] Support for A-Level and international exam boards (CIE, Edexcel International).
- [ ] Rate limiting and authentication middleware.

---

## ⚖️ Disclaimer

This application is designed as an educational assistant and revision aid. Grades and marks generated by AI are estimates and should not replace accredited assessment by official exam board examiners.
