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
    st.write("Category:", category)
    st.write("Sentiment:", sentiment)
    st.write("Priority:", priority)

st.subheader("Email History")

try:
    df = pd.read_csv("data/email.csv")

    st.dataframe(df)

    st.subheader("Category Distribution")

    category_counts = df["category"].value_counts()

    st.write(category_counts)

    st.bar_chart(category_counts)

except Exception as e:
    st.error(f"Error: {e}")