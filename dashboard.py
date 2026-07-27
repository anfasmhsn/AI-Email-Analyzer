import streamlit as st
import pandas as pd

from classifier import classify_email
from sentiment import get_sentiment
from priority import get_priority
from database import save_email, get_emails
from gmail_fetch import fetch_emails
st.title("📧 SmartMail AI")
if st.button("📥 Import Gmail"):

    emails = fetch_emails()

    for mail in emails:

        text = mail["subject"] + " " + mail["body"]

        category = classify_email(text)

        sentiment = get_sentiment(text)

        priority = get_priority(
            text,
            category,
            sentiment
        )

        save_email(
            mail["sender"],
            mail["subject"],
            mail["body"],
            category,
            sentiment,
            priority,
            mail["date"]
        )
    st.success("Emails Imported Successfully!")
email = st.text_area("Enter Email")

if st.button("Analyze"):

    category = classify_email(email)
    sentiment = get_sentiment(email)
    priority = get_priority(email, category, sentiment)

    save_email(
        email,
        category,
        sentiment,
        priority
    )

    st.success("Analysis Complete")

    st.write("### Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Category", category)
    col2.metric("Sentiment", sentiment)
    col3.metric("Priority", priority)

    summary = f"""
    This email was classified as {category}.
    The detected sentiment is {sentiment}.
    Priority level is {priority}.
    """

    st.subheader("AI Summary")
    st.info(summary)

    st.subheader("Email History")

try:
    emails = get_emails()

    df = pd.DataFrame(
        emails,
        columns=[
            "id",
            "sender",
            "subject",
            "body",
            "category",
            "sentiment",
            "priority",
            "date"
        ]
    )
    search = st.text_input("🔍 Search Emails")

    if search:
        df = df[
            df["subject"].str.contains(search, case=False, na=False)
            |
            df["sender"].str.contains(search, case=False, na=False)
            ]
    selected_category = st.selectbox(
        "Filter Category",
        ["All"] + list(df["category"].unique())
    )

    if selected_category != "All":
        df = df[
            df["category"] == selected_category
    ]    
    st.dataframe(df)

    st.subheader("Category Distribution")
    category_counts = df["category"].value_counts()
    st.write(category_counts)
    st.bar_chart(category_counts)

    st.subheader("Priority Distribution")
    priority_counts = df["priority"].value_counts()
    st.bar_chart(priority_counts)

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="email_report.csv",
        mime="text/csv"
    )
except Exception as e:
    st.error(f"Error: {e}")