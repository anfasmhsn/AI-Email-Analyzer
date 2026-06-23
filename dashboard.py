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

    st.subheader("Email History")

try:
    df = pd.read_csv("data/email.csv")

    st.dataframe(df)

    st.subheader("Category Distribution")
    category_counts = df["category"].value_counts()
    st.write(category_counts)
    st.bar_chart(category_counts)

    st.subheader("Priority Distribution")
    priority_counts = df["priority"].value_counts()
    st.bar_chart(priority_counts)

except Exception as e:
    st.error(f"Error: {e}")