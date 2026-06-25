import re


ROLE_SKILLS = {
    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Responsive Design",
        "Git",
        "REST APIs",
        "Accessibility",
        "Testing",
    ],
    "Backend Developer": [
        "Python",
        "Flask",
        "Django",
        "REST APIs",
        "SQL",
        "Databases",
        "Authentication",
        "Git",
        "API Design",
        "Unit Testing",
    ],
    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Python",
        "REST APIs",
        "SQL",
        "Databases",
        "Git",
        "Deployment",
    ],
    "Data Analyst": [
        "Excel",
        "SQL",
        "Python",
        "Pandas",
        "Data Visualization",
        "Power BI",
        "Tableau",
        "Statistics",
        "Dashboarding",
    ],
    "AI/ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "Model Evaluation",
        "MLOps",
    ],
}


SKILL_KEYWORDS = {
    "JavaScript": ["javascript", "js", "ecmascript"],
    "React": ["react", "reactjs", "react.js"],
    "Responsive Design": ["responsive", "mobile first", "media queries"],
    "REST APIs": ["rest", "rest api", "restful", "api"],
    "Accessibility": ["accessibility", "a11y", "wcag"],
    "Testing": ["testing", "jest", "cypress", "playwright"],
    "Databases": ["database", "databases", "postgresql", "mysql", "mongodb"],
    "Authentication": ["authentication", "authorization", "jwt", "oauth"],
    "API Design": ["api design", "api development", "endpoint"],
    "Unit Testing": ["unit test", "unit testing", "pytest", "unittest"],
    "Node.js": ["node.js", "nodejs", "node"],
    "Deployment": ["deployment", "docker", "ci/cd", "hosting"],
    "Excel": ["excel", "spreadsheet", "pivot table"],
    "Data Visualization": ["data visualization", "visualisation", "charts", "matplotlib", "seaborn"],
    "Power BI": ["power bi", "powerbi"],
    "Dashboarding": ["dashboard", "dashboards", "reporting"],
    "Machine Learning": ["machine learning", "ml", "supervised learning"],
    "Deep Learning": ["deep learning", "neural network", "cnn", "rnn"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "NumPy": ["numpy", "np"],
    "Model Evaluation": ["model evaluation", "metrics", "accuracy", "precision", "recall"],
    "MLOps": ["mlops", "model deployment", "model monitoring"],
}


def get_supported_roles():
    return list(ROLE_SKILLS.keys())


def is_supported_role(job_role):
    return job_role in ROLE_SKILLS


def analyze_resume(resume_text, job_role):
    normalized_text = _normalize(resume_text)
    required_skills = ROLE_SKILLS[job_role]

    matched_skills = [
        skill for skill in required_skills if _contains_skill(normalized_text, skill)
    ]
    missing_skills = [skill for skill in required_skills if skill not in matched_skills]

    match_score = round((len(matched_skills) / len(required_skills)) * 100)
    ats_score = _calculate_ats_score(normalized_text, match_score)
    suggestions = _build_suggestions(job_role, missing_skills, normalized_text)

    return {
        "job_role": job_role,
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "improvement_suggestions": suggestions,
        # Existing frontend aliases.
        "ats_score": ats_score,
        "strengths": matched_skills,
        "suggestions": suggestions,
        "summary": _build_summary(job_role, matched_skills, missing_skills, match_score),
    }


def _normalize(text):
    return re.sub(r"\s+", " ", text.lower())


def _contains_skill(text, skill):
    keywords = [skill.lower()] + [keyword.lower() for keyword in SKILL_KEYWORDS.get(skill, [])]

    for keyword in keywords:
        pattern = rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])"
        if re.search(pattern, text):
            return True

    return False


def _calculate_ats_score(text, match_score):
    important_sections = ["skills", "experience", "projects", "education"]
    section_score = sum(1 for section in important_sections if section in text) * 5
    length_score = 10 if len(text.split()) >= 250 else 5
    return min(100, round(match_score * 0.75 + section_score + length_score))


def _build_suggestions(job_role, missing_skills, text):
    suggestions = []

    for skill in missing_skills[:5]:
        suggestions.append(
            f"Add clear evidence of {skill} through projects, coursework, internships, or work experience."
        )

    if "project" not in text:
        suggestions.append("Add a projects section with role-relevant work and links to demos or GitHub.")

    if not any(word in text for word in ["improved", "reduced", "increased", "built", "created"]):
        suggestions.append("Use action verbs and measurable impact, such as improved speed by 30%.")

    suggestions.append(f"Tailor your summary and skills section toward the {job_role} role.")

    return suggestions


def _build_summary(job_role, matched_skills, missing_skills, match_score):
    if matched_skills:
        strongest = ", ".join(matched_skills[:4])
    else:
        strongest = "no major required skills detected yet"

    if missing_skills:
        gaps = ", ".join(missing_skills[:4])
        return (
            f"Your resume has a {match_score}% match for {job_role}. "
            f"Strong signals include {strongest}. Focus next on {gaps}."
        )

    return (
        f"Your resume has a {match_score}% match for {job_role}. "
        f"It already covers the main required skills, especially {strongest}."
    )
