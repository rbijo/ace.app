# ACE Backend API

FastAPI backend service powering the ACE academic workflow engine, AI tutoring service, progress calculation, and flowchart topic roadmap system.

## Setup & Running

1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Application**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
4. **API Documentation**:
   Interactive Swagger docs are available at `http://localhost:8000/docs`.

## Key Modules

- `app/models/`: SQLAlchemy 2.x data models for User, Course, Subject, Topic (flowchart nodes), Task, Progress, and AISession.
- `app/services/learning_service.py`: Computes roadmap flowchart nodes and prerequisite links.
- `app/services/progress_service.py`: Calculates dynamic completion percentages per subject.
- `app/services/ai/`: Extensible AI service abstraction (OpenRouter, Gemini, OpenAI).
