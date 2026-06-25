TECHNICAL_QUESTIONS = {
    "Frontend Developer": [
        "How do HTML, CSS, and JavaScript work together in a modern web page?",
        "Explain the difference between props and state in React.",
        "How would you make a page responsive across mobile and desktop screens?",
        "What steps do you take to improve frontend performance?",
        "How do you consume and handle errors from a REST API?",
    ],
    "Backend Developer": [
        "Explain how a REST API request flows from route to response.",
        "How would you design authentication for a Flask application?",
        "What is the difference between SQL and NoSQL databases?",
        "How do you handle validation and error responses in an API?",
        "How would you test backend services and endpoints?",
    ],
    "Full Stack Developer": [
        "How do you connect a frontend form to a backend API?",
        "Explain how you would structure a full stack feature from UI to database.",
        "How do you manage authentication across frontend and backend?",
        "What are common causes of slow full stack applications?",
        "How would you deploy a full stack web app?",
    ],
    "Data Analyst": [
        "How do you clean and validate a messy dataset?",
        "Explain joins in SQL with a practical example.",
        "How do you choose the right chart for a business question?",
        "What is the difference between correlation and causation?",
        "How would you explain a dashboard insight to a non-technical stakeholder?",
    ],
    "AI/ML Engineer": [
        "What is the difference between supervised and unsupervised learning?",
        "How do you prevent overfitting in a machine learning model?",
        "Explain precision, recall, and F1 score.",
        "How would you deploy and monitor an ML model?",
        "When would you choose TensorFlow, PyTorch, or Scikit-learn?",
    ],
}


BEHAVIORAL_QUESTIONS = [
    "Tell me about a time you learned a new technology quickly.",
    "Describe a project where you solved a difficult problem.",
    "How do you handle feedback on your work?",
    "Tell me about a time you worked with a teammate who had a different opinion.",
    "How do you prioritize tasks when deadlines are close?",
]


HR_QUESTIONS = [
    "Tell me about yourself.",
    "Why are you interested in this role?",
    "What are your strengths and areas for improvement?",
    "Where do you see yourself in the next two years?",
    "Why should we select you for this position?",
]


def generate_interview_questions(job_role):
    return {
        "job_role": job_role,
        "technical_questions": TECHNICAL_QUESTIONS[job_role],
        "behavioral_questions": BEHAVIORAL_QUESTIONS,
        "hr_questions": HR_QUESTIONS,
    }
