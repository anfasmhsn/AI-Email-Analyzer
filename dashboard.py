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
        sender,
        subject,
        body,
        category,
        sentiment,
        priority,
        date
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
    df["Select"] = False
    priority_order = {
    "High": 0,
    "Medium": 1,
    "Low": 2
    }

    df["priority_order"] = df["priority"].map(priority_order)

    df = df.sort_values("priority_order")

    df = df.drop(columns=["priority_order"])
    total_emails = len(df)
    
    high_priority = len(
        df[df["priority"] == "High"]
        )
    
    total_categories = df["category"].nunique()
    
    if not df.empty:
        top_sender = df["sender"].value_counts().idxmax()
    else:
        top_sender = "N/A"
    
    st.subheader("Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📧 Total Emails",
        total_emails
    )

    col2.metric(
        "🔥 High Priority",
        high_priority
    )

    col3.metric(
        "📂 Categories",
        total_categories
    )

    col4.metric(
        "👤 Top Sender",
        top_sender
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
    edited_df = st.data_editor(
        df,
        hide_index=True,
        use_container_width=True
    )
    selected_rows = edited_df[
        edited_df["Select"] == True
    ]
    st.write(f"Selected Emails: {len(selected_rows)}")
    if st.button("🗑 Delete Selected"):
        st.write(selected_rows)
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