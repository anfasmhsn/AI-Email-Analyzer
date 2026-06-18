import streamlit as st

from classifier import classify_email
from sentiment import get_sentiment
from priority import get_priority

st.title("📧 SmartMail AI")

email = st.text_area("Enter Email")

if st.button("Analyze"):

    category = classify_email(email)
    sentiment = get_sentiment(email)
    priority = get_priority(email, category, sentiment)

    st.success("Analysis Complete")

    st.write("### Results")
    st.write("Category:", category)
    st.write("Sentiment:", sentiment)
    st.write("Priority:", priority)