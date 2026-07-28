import os
import pandas as pd
import streamlit as st
from modules.calendar_scheduler import schedule_interview
from modules.dataset import load_dataset
from modules.email_sender import send_email
from modules.process_candidates import process_candidates
from modules.resume_downloader import download_all_resumes

# =====================================
# Page Configuration
# =====================================
st.set_page_config(
    page_title="AI Candidate Screening", page_icon="🤖", layout="wide"
)

# =====================================
# Session State Initialization
# =====================================
if "screened_df" not in st.session_state:
    st.session_state.screened_df = None

if "emails_sent" not in st.session_state:
    st.session_state.emails_sent = False

# =====================================
# Title
# =====================================
st.title("🤖 AI Candidate Screening Platform")
st.write("Upload a candidate dataset and let AI rank the resumes.")

st.divider()

# =====================================
# Upload Dataset
# =====================================
st.subheader("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload Candidate Dataset", type=["xlsx", "csv"]
)

# =====================================
# Continue only after upload
# =====================================
if uploaded_file is not None:

    # Load initial dataset
    df = load_dataset(uploaded_file)

    st.success("✅ Dataset uploaded successfully!")
    st.divider()

    # =====================================
    # Display Uploaded Candidate Dataset
    # =====================================
    st.subheader("📋 Candidate Dataset")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # =====================================
    # Job Description Input
    # =====================================
    st.subheader("📝 Job Description")

    job_description = st.text_area(
        "Paste the Job Description Here",
        value="""
Looking for an AI/ML Engineer.

Required Skills:
- Python
- Machine Learning
- Deep Learning
- NLP
- TensorFlow
- SQL

Responsibilities:
- Build ML models
- Work on AI projects
- Research new AI techniques
""",
        height=220,
    )

    st.divider()

    # =====================================
    # AI Resume Screening Trigger
    # =====================================
    st.subheader("🚀 AI Resume Screening")

    if st.button("🚀 Start AI Screening"):
        with st.spinner("Screening Candidates..."):
            try:
                processed_df = process_candidates(df, job_description)

                # Sort candidates by Resume Score descending
                processed_df = processed_df.sort_values(
                    by="Resume Score", ascending=False
                ).reset_index(drop=True)

                # Save to session_state so interaction doesn't wipe state
                st.session_state.screened_df = processed_df
                st.success("✅ Screening Completed!")

            except Exception as e:
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    st.error(
                        "⚠️ Gemini API quota exceeded.\n\nPlease wait until your quota resets or use another API Key."
                    )
                else:
                    st.error(f"❌ AI Screening Failed\n\n{e}")
                st.stop()

    # =====================================
    # Results View (Triggered after Screening)
    # =====================================
    if st.session_state.screened_df is not None:
        result_df = st.session_state.screened_df

        # =====================================
        # Screening Summary
        # =====================================
        st.divider()
        st.subheader("📊 Screening Summary")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Candidates", len(result_df))
        col2.metric(
            "Average Score", round(result_df["Resume Score"].mean(), 1)
        )
        col3.metric("Highest Score", result_df["Resume Score"].max())
        col4.metric("Lowest Score", result_df["Resume Score"].min())

        # =====================================
        # Search & Filter Controls
        # =====================================
        st.divider()
        search = st.text_input("🔍 Search Candidate")

        if search:
            filtered_df = result_df[
                result_df["name"].str.contains(search, case=False, na=False)
            ]
        else:
            filtered_df = result_df

        minimum_score = st.slider("Minimum Resume Score", 0, 100, 0)

        filtered_df = filtered_df[
            filtered_df["Resume Score"] >= minimum_score
        ]

        # =====================================
        # Ranked Candidates Table
        # =====================================
        st.divider()
        st.subheader("🏆 Ranked Candidates")

        display_columns = [
            "name",
            "Resume Score",
            "GitHub Score",
            "Recommendation",
        ]

        # Filter display columns safely in case certain keys are missing
        existing_cols = [
            col for col in display_columns if col in filtered_df.columns
        ]

        st.dataframe(
            filtered_df[existing_cols],
            use_container_width=True,
        )

        # =====================================
        # Top 5 Candidates
        # =====================================
        st.divider()
        st.subheader("🏆 Top 5 Candidates")

        top5 = filtered_df.head(5)

        st.dataframe(
            top5[existing_cols],
            use_container_width=True,
        )

        # =====================================
        # Send Assessment Emails
        # =====================================
        st.divider()
        st.subheader("📧 Send Assessment Emails")

        test_link = st.text_input(
            "Assessment Link", value="https://forms.gle/demo123"
        )

        send_button = st.button(
            "📧 Send Emails to Top 5 Candidates",
            disabled=top5.empty or st.session_state.emails_sent,
        )

        if send_button:
            if "email" not in top5.columns:
                st.error("❌ 'email' column not found in the uploaded dataset.")
            else:
                with st.spinner("Sending emails..."):
                    success = 0
                    failed = 0

                    for _, row in top5.iterrows():
                        email = str(row.get("email", "")).strip()

                        # Skip if email is missing
                        if not email:
                            st.warning(
                                f"⚠️ Skipped {row.get('name', 'Candidate')} (No email address)"
                            )
                            failed += 1
                            continue

                        try:
                            send_email(
                                receiver_email=email,
                                candidate_name=row.get("name", "Candidate"),
                                test_link=test_link,
                            )
                            success += 1
                        except Exception as e:
                            failed += 1
                            st.error(
                                f"❌ Failed to send email to {row.get('name', 'Candidate')}"
                            )
                            st.exception(e)

                st.success(f"✅ {success} email(s) sent successfully!")

                if failed > 0:
                    st.warning(f"⚠️ {failed} email(s) could not be sent.")

                # Disable button after sending
                st.session_state.emails_sent = True

        # Reset button
        if st.session_state.emails_sent:
            if st.button("🔄 Enable Email Sending Again"):
                st.session_state.emails_sent = False
                st.rerun()

        # =====================================
        # Candidate Recommendation Cards
        # =====================================
        st.divider()
        st.subheader("👤 Candidate Recommendations")

        for _, row in top5.iterrows():
            st.info(
                f"""
### 👤 {row.get('name', 'N/A')}

⭐ **Resume Score** : {row.get('Resume Score', 'N/A')}  
💻 **GitHub Score** : {row.get('GitHub Score', 'N/A')}  
📌 **Recommendation** : {row.get('Recommendation', 'N/A')}
"""
            )

            with st.expander("📝 AI GitHub Analysis"):
                st.write(
                    row.get(
                        "GitHub Summary", "No GitHub analysis available."
                    )
                )

        # =====================================
        # Upload Test Results & Final Ranking
        # =====================================
        st.divider()
        st.subheader("📄 Upload Test Results")

        test_file = st.file_uploader(
            "Upload Test Results CSV", type=["csv"], key="test_results"
        )

        final_df = filtered_df.copy()

        if test_file is not None:
            try:
                test_df = pd.read_csv(test_file)
                st.success("✅ Test results uploaded!")

                st.dataframe(test_df, use_container_width=True)

                merged_df = filtered_df.merge(test_df, on="name", how="left")

                if "Test Score" not in merged_df.columns:
                    merged_df["Test Score"] = 0
                else:
                    merged_df["Test Score"] = merged_df["Test Score"].fillna(0)

                # Ensure numerical scores for calculation
                resume_sc = merged_df.get("Resume Score", 0).fillna(0)
                github_sc = merged_df.get("GitHub Score", 0).fillna(0)
                test_sc = merged_df["Test Score"]

                merged_df["Final Score"] = (
                    resume_sc * 0.5 + github_sc * 0.2 + test_sc * 0.3
                )

                merged_df = merged_df.sort_values(
                    "Final Score", ascending=False
                )

                st.subheader("🏆 Final Candidate Ranking")

                ranking_cols = [
                    col
                    for col in [
                        "name",
                        "Resume Score",
                        "GitHub Score",
                        "Test Score",
                        "Final Score",
                    ]
                    if col in merged_df.columns
                ]

                st.dataframe(
                    merged_df[ranking_cols],
                    use_container_width=True,
                )
                final_df = merged_df

            except Exception as e:
                st.error(f"❌ Error processing test results CSV: {e}")

        # =====================================
        # Interview Scheduler
        # =====================================
        st.divider()
        st.subheader("📅 Interview Scheduler")

        if not final_df.empty and "name" in final_df.columns:
            selected_candidate = st.selectbox(
                "Select Candidate", final_df["name"]
            )

            candidate_row = final_df[
                final_df["name"] == selected_candidate
            ].iloc[0]

            interview_date = st.date_input("Interview Date")
            interview_time = st.time_input("Interview Time")

            if st.button("📅 Schedule Interview"):
                candidate_email = candidate_row.get("email")

                if not candidate_email or pd.isna(candidate_email):
                    st.error("❌ Selected candidate does not have a valid email address.")
                else:
                    with st.spinner("Scheduling Interview..."):
                        try:
                            meet_link = schedule_interview(
                                candidate_name=candidate_row["name"],
                                candidate_email=str(candidate_email).strip(),
                                interview_date=interview_date,
                                interview_time=interview_time,
                            )

                            st.success("✅ Interview Scheduled Successfully!")
                            st.write("### 🎥 Google Meet Link")
                            st.code(meet_link)

                        except Exception as e:
                            st.error(f"❌ Failed to schedule interview: {e}")

        # =====================================
        # Candidate Scores Bar Chart
        # =====================================
        st.divider()
        st.subheader("📊 Candidate Scores")

        if not final_df.empty and "name" in final_df.columns:
            possible_chart_cols = [
                "Resume Score",
                "GitHub Score",
                "Test Score",
                "Final Score",
            ]
            chart_cols = [
                col for col in possible_chart_cols if col in final_df.columns
            ]

            if chart_cols:
                chart_data = final_df.set_index("name")[chart_cols]
                st.bar_chart(chart_data)

        # =====================================
        # Download Results (CSV)
        # =====================================
        st.divider()
        csv = final_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Results",
            data=csv,
            file_name="candidate_ranking.csv",
            mime="text/csv",
        )

        # =====================================
        # Resume Downloader Section
        # =====================================
        st.divider()
        st.subheader("📄 Resume Downloader")

        if st.button("📥 Download All Resumes"):
            with st.spinner("Downloading Resumes..."):
                download_all_resumes(final_df)
            st.success("✅ All resumes downloaded successfully!")