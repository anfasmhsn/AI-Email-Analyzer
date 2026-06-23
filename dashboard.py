import streamlit as st
import pandas as pd

from classifier import classify_email
from sentiment import get_sentiment
from priority import get_priority
from save_email import save_email
st.title("📧 SmartMail AI")

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
    df = pd.read_csv("data/email.csv")
    search = st.text_input("🔍 Search Emails")

    if search:
        df = df[
            df["email"].str.contains(
                search,
                case=False,
                na=False
            )
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