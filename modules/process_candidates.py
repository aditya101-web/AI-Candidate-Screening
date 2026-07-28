import re
import pandas as pd
from modules.ai_scoring import score_resume
from modules.fallback_scoring import rule_based_score
from modules.github_ai import analyze_github_profile
from modules.github_analysis import get_repositories, github_score
from modules.resume_downloader import download_resume
from modules.resume_parser import parse_resume


def process_candidates(df, job_description):
    df.columns = df.columns.str.strip().str.lower()

    resume_scores = []
    recommendations = []
    github_scores = []
    github_summaries = []

    for _, row in df.iterrows():

        # ----------------------------
        # Candidate Details
        # ----------------------------
        candidate_name = row["name"]
        resume_link = row["resume"]
        github_url = row.get("github", None)

        # ----------------------------
        # Download Resume
        # ----------------------------
        resume_path = download_resume(resume_link, candidate_name)

        if resume_path is None:
            resume_scores.append(0)
            github_scores.append(0)
            recommendations.append("❌ Resume Download Failed")
            github_summaries.append(
                "No GitHub summary available (Download Failed)."
            )
            continue

        # ----------------------------
        # Parse Resume
        # ----------------------------
        resume_text = parse_resume(resume_path)

        # ----------------------------
        # GitHub Analysis
        # ----------------------------
        repos = []
        summary = "No GitHub URL provided."

        if pd.notna(github_url) and str(github_url).strip():
            try:
                # Fetch repositories from GitHub URL
                repos = get_repositories(github_url) or []
                github_score_value = github_score(repos)

                if repos:
                    try:
                        summary = analyze_github_profile(repos)
                    except Exception as e:
                        print(
                            f"GitHub AI analysis failed for {candidate_name}: {e}"
                        )
                        summary = "GitHub AI analysis failed."
                else:
                    summary = "No public GitHub repositories found."

            except Exception as e:
                print(f"Error fetching GitHub data for {candidate_name}: {e}")
                repos = []
                github_score_value = 0
                summary = "Error analyzing GitHub profile."
        else:
            github_score_value = 0

        # Append summary safely
        github_summaries.append(summary)

        # ----------------------------
        # AI Resume Scoring
        # ----------------------------
        try:
            result = score_resume(job_description, resume_text)
            match = re.search(r"Resume Score:\s*(\d+)", result)

            if match:
                score = int(match.group(1))
            else:
                score = rule_based_score(resume_text, job_description)

        except Exception:
            print("Gemini failed. Using fallback scoring.")
            score = rule_based_score(resume_text, job_description)

        # ----------------------------
        # Final Score
        # ----------------------------
        final_score = int((score * 0.7) + (github_score_value * 0.3))

        # ----------------------------
        # Recommendation
        # ----------------------------
        if final_score >= 90:
            recommendation = "⭐ Strongly Recommended"
        elif final_score >= 75:
            recommendation = "📞 Technical Interview"
        elif final_score >= 60:
            recommendation = "📋 HR Interview"
        else:
            recommendation = "❌ Reject"

        # ----------------------------
        # Save Results
        # ----------------------------
        resume_scores.append(final_score)
        github_scores.append(github_score_value)
        recommendations.append(recommendation)

    # ----------------------------
    # Add Columns
    # ----------------------------
    df["Resume Score"] = resume_scores
    df["GitHub Score"] = github_scores
    df["Recommendation"] = recommendations
    df["GitHub Summary"] = github_summaries

    # ----------------------------
    # Rank Candidates
    # ----------------------------
    df = df.sort_values(by="Resume Score", ascending=False).reset_index(
        drop=True
    )

    return df