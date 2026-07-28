from modules.ai_scoring import client


def analyze_github_profile(repositories):

    repo_text = ""

    for repo in repositories[:5]:

        repo_text += f"""

Repository Name:
{repo['name']}

Description:
{repo['description']}

Language:
{repo['language']}

Stars:
{repo['stars']}

Forks:
{repo['forks']}

"""

    prompt = f"""
You are an HR Technical Recruiter.

Analyze the following GitHub repositories.

{repo_text}

Give:

Overall GitHub Score (0-100)

Strengths

Weaknesses

Technical Skills

Recommendation

Return in professional format.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text