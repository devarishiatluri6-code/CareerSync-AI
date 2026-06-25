ROADMAPS = {
    "Frontend Developer": {
        "beginner_topics": ["HTML semantics", "CSS layouts", "JavaScript fundamentals", "Git basics"],
        "intermediate_topics": ["React components", "State management", "REST API integration", "Accessibility"],
        "projects_to_build": ["Portfolio website", "Weather app with API", "Responsive dashboard"],
        "preparation_tips": ["Practice DOM and React questions", "Improve UI polish", "Deploy projects online"],
        "certifications": ["Meta Front-End Developer", "freeCodeCamp Responsive Web Design"],
        "resources": ["MDN Web Docs", "React documentation", "Frontend Mentor"],
    },
    "Backend Developer": {
        "beginner_topics": ["Python fundamentals", "HTTP basics", "Flask routing", "SQL basics"],
        "intermediate_topics": ["REST API design", "Authentication", "Database modeling", "Unit testing"],
        "projects_to_build": ["Task manager API", "Auth-based notes app", "Resume analysis API"],
        "preparation_tips": ["Practice API design problems", "Write tests for each endpoint", "Learn logging and errors"],
        "certifications": ["Python Institute PCAP", "PostgreSQL fundamentals"],
        "resources": ["Flask documentation", "Real Python", "SQLBolt"],
    },
    "Full Stack Developer": {
        "beginner_topics": ["HTML/CSS/JS", "Python or Node.js", "Git", "Basic SQL"],
        "intermediate_topics": ["React", "REST APIs", "Authentication", "Deployment"],
        "projects_to_build": ["Job tracker app", "E-commerce mini app", "Full stack dashboard"],
        "preparation_tips": ["Explain end-to-end feature flow", "Deploy one complete app", "Practice debugging across layers"],
        "certifications": ["freeCodeCamp Full Stack Developer", "Meta Front-End Developer"],
        "resources": ["MDN Web Docs", "Flask documentation", "Full Stack Open"],
    },
    "Data Analyst": {
        "beginner_topics": ["Excel", "SQL SELECT queries", "Statistics basics", "Data cleaning"],
        "intermediate_topics": ["Pandas", "Data visualization", "Power BI or Tableau", "Dashboard storytelling"],
        "projects_to_build": ["Sales dashboard", "Customer churn analysis", "Excel to SQL reporting project"],
        "preparation_tips": ["Practice SQL daily", "Tell clear stories from charts", "Prepare business case studies"],
        "certifications": ["Google Data Analytics", "Microsoft Power BI Data Analyst"],
        "resources": ["Kaggle datasets", "Mode SQL tutorial", "Microsoft Learn Power BI"],
    },
    "AI/ML Engineer": {
        "beginner_topics": ["Python", "Linear algebra basics", "Statistics", "Pandas and NumPy"],
        "intermediate_topics": ["Machine learning algorithms", "Deep learning", "Model evaluation", "MLOps basics"],
        "projects_to_build": ["Prediction model API", "Image classifier", "Recommendation system"],
        "preparation_tips": ["Explain model tradeoffs", "Track experiments", "Deploy one ML model as an API"],
        "certifications": ["DeepLearning.AI Machine Learning", "TensorFlow Developer Certificate"],
        "resources": ["Scikit-learn documentation", "Kaggle", "DeepLearning.AI short courses"],
    },
}


def generate_roadmap(job_role, missing_skills):
    base = ROADMAPS[job_role]
    focus_skills = _unique(missing_skills + base["intermediate_topics"] + base["beginner_topics"])

    timeline = [
        f"Week 1-2: Strengthen basics: {', '.join(base['beginner_topics'][:3])}.",
        f"Week 3-4: Focus on missing skills: {', '.join(focus_skills[:4])}.",
        f"Week 5-6: Build and document a project: {base['projects_to_build'][0]}.",
        "Week 7-8: Revise interview questions, improve resume bullets, and deploy your best project.",
    ]

    return {
        "job_role": job_role,
        "missing_skills": missing_skills,
        "beginner_topics": base["beginner_topics"],
        "intermediate_topics": base["intermediate_topics"],
        "projects_to_build": base["projects_to_build"],
        "preparation_tips": base["preparation_tips"],
        # Existing frontend aliases.
        "timeline": timeline,
        "skills": focus_skills,
        "certifications": base["certifications"],
        "projects": base["projects_to_build"],
        "resources": base["resources"],
    }


def _unique(items):
    seen = set()
    ordered = []

    for item in items:
        if item and item not in seen:
            ordered.append(item)
            seen.add(item)

    return ordered
