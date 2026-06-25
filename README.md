# CareerSync AI

CareerSync AI is a mini web app that analyzes resumes for selected job roles, generates interview questions, and creates a personalized learning roadmap.

## Run the Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The Flask backend runs at:

```text
http://localhost:5000
```

## API Endpoints

- `POST /api/analyze` accepts a resume file (`resume`) and job role (`job_role` or `role`).
- `POST /api/interview` accepts a job role and returns technical, behavioral, and HR questions.
- `POST /api/roadmap` accepts a job role and missing skills list, then returns a personalized roadmap.

Supported resume formats: PDF, DOCX, and TXT.

Supported roles:

- Frontend Developer
- Backend Developer
- Full Stack Developer
- Data Analyst
- AI/ML Engineer
