import re

def rule_based_score(resume_text, job_description):

    job_skills = [
        skill.strip().lower()
        for skill in re.split(r"[,\\n-]+", job_description)
        if len(skill.strip()) > 2
    ]

    resume = resume_text.lower()

    matched = 0

    for skill in job_skills:

        if skill in resume:
            matched += 1

    if len(job_skills) == 0:
        return 0

    score = int((matched / len(job_skills)) * 100)

    return score