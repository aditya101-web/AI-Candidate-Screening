
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
def score_resume(job_description, resume_text):

    prompt = f"""
You are an HR recruiter.

Compare the following resume with the job description.

Job Description:
{job_description}

Resume:
{resume_text}

Give the following:

1. Resume Score out of 100

2. Strengths

3. Weaknesses

4. Missing Skills

Return the answer in a professional format.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text
if __name__ == "__main__":

    job_description = """
    Looking for an AI/ML Engineer.

    Skills:
    Python
    Machine Learning
    Deep Learning
    NLP
    TensorFlow
    SQL
    """

    resume_text = """
    Skills

    Python
    Machine Learning
    TensorFlow
    SQL

    Projects

    Breast Cancer Detection using CNN

    Education

    B.Tech AI & ML
    """

    result = score_resume(job_description, resume_text)

    print(result)
