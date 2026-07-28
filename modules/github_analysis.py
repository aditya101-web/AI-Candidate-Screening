import requests


def get_repositories(profile_url):

    username = profile_url.rstrip("/").split("/")[-1]

    repo_url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(repo_url)

    if response.status_code != 200:
        return None

    repos = response.json()

    repository_data = []

    for repo in repos:
        repository_data.append({
            "name": repo["name"],
            "description": repo["description"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "updated": repo["updated_at"],
            "topics": repo.get("topics", []),
            "url": repo["html_url"]
        })

    return repository_data


def github_score(repositories):

    if not repositories:
        return 0

    total_repos = len(repositories)
    total_stars = 0
    python_repos = 0
    documented_projects = 0

    for repo in repositories:
        total_stars += repo["stars"]

        if repo["language"] == "Python":
            python_repos += 1

        if repo["description"]:
            documented_projects += 1

    score = 0
    score += min(total_repos * 2, 30)
    score += min(total_stars, 20)
    score += min(python_repos * 5, 30)
    score += min(documented_projects * 2, 20)

    return min(score, 100)