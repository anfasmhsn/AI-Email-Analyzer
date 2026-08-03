import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from classifier import classify_email
from sentiment import get_sentiment
from priority import get_priority
from database import save_email, get_emails, delete_selected
from gmail_fetch import fetch_emails

st.title("📧 SmartMail AI")

# -------------------------------------------------------
# IMPORT GMAIL
# -------------------------------------------------------

if st.button("📥 Import Gmail"):

    emails = fetch_emails()

    for mail in emails:

        text = mail["subject"] + " " + mail["body"]

        category = classify_email(text)
        sentiment = get_sentiment(text)
        priority = get_priority(text, category, sentiment)

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

# -------------------------------------------------------
# ANALYZE MANUAL EMAIL
# -------------------------------------------------------

email = st.text_area("Enter Email")

if st.button("Analyze"):

    category = classify_email(email)
    sentiment = get_sentiment(email)
    priority = get_priority(email, category, sentiment)

    st.success("Analysis Complete")

    col1, col2, col3 = st.columns(3)

    col1.metric("Category", category)
    col2.metric("Sentiment", sentiment)
    col3.metric("Priority", priority)

    st.subheader("AI Summary")

    st.info(f"""
Category : {category}

Sentiment : {sentiment}

Priority : {priority}
""")

# -------------------------------------------------------
# LOAD EMAILS
# -------------------------------------------------------

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

    # ---------------------------------------------------
    # SORT PRIORITY
    # ---------------------------------------------------

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    df["priority_order"] = df["priority"].map(priority_order)

    df = df.sort_values("priority_order")

    df = df.drop(columns=["priority_order"])

    # ---------------------------------------------------
    # DASHBOARD METRICS
    # ---------------------------------------------------

    total_emails = len(df)

    high_priority = len(
        df[df["priority"] == "High"]
    )

    total_categories = df["category"].nunique()

    if df.empty:
        top_sender = "N/A"
    else:
        top_sender = df["sender"].value_counts().idxmax()

    st.subheader("📊 Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📧 Total Emails", total_emails)
    c2.metric("🔥 High Priority", high_priority)
    c3.metric("📂 Categories", total_categories)
    c4.metric("👤 Top Sender", top_sender)

    # ---------------------------------------------------
    # SEARCH
    # ---------------------------------------------------

    search = st.text_input("🔍 Search Emails")

    if search:

        df = df[
            df["subject"].str.contains(search, case=False, na=False)
            |
            df["sender"].str.contains(search, case=False, na=False)
        ]

    # ---------------------------------------------------
    # FILTER
    # ---------------------------------------------------

    selected_category = st.selectbox(
        "Filter Category",
        ["All"] + list(df["category"].unique())
    )

    if selected_category != "All":

        df = df[
            df["category"] == selected_category
        ]

    # ---------------------------------------------------
    # AGGRID
    # ---------------------------------------------------
    from st_aggrid import AgGrid, GridOptionsBuilder

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        editable=False,
        groupable=False
    )

    gb.configure_selection(
        "multiple",
        use_checkbox=True,
        pre_selected_rows=[]
    )

    gb.configure_grid_options(
        rowSelection="multiple"
    )

    grid = AgGrid(
        df,
        gridOptions=gb.build(),
        enable_enterprise_modules=False,
        height=500,
    )
    # ---------------------------------------------------
# DELETE
# ---------------------------------------------------

    if st.button("🗑 Delete Selected"):

        selected = grid["selected_rows"]

        if selected is None:
            st.warning("Please select at least one email.")

        elif isinstance(selected, pd.DataFrame):

            if selected.empty:
                st.warning("Please select at least one email.")

            else:
                ids = selected["id"].tolist()

                delete_selected(ids)

                st.success("Selected Emails Deleted!")

                st.rerun()

        elif isinstance(selected, list):

            if len(selected) == 0:
                st.warning("Please select at least one email.")

            else:
                ids = [row["id"] for row in selected]

                delete_selected(ids)

                st.success("Selected Emails Deleted!")

                st.rerun()
    # ---------------------------------------------------
    # CATEGORY CHART
    # ---------------------------------------------------

    st.subheader("Category Distribution")

    category_counts = df["category"].value_counts()

    st.write(category_counts)

    st.bar_chart(category_counts)

    # ---------------------------------------------------
    # PRIORITY CHART
    # ---------------------------------------------------

    st.subheader("Priority Distribution")

    priority_counts = (
        df["priority"]
        .value_counts()
        .reindex(["High", "Medium", "Low"])
        .fillna(0)
    )

    st.bar_chart(priority_counts)

    # ---------------------------------------------------
    # DOWNLOAD
    # ---------------------------------------------------

    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Report",
        csv,
        "email_report.csv",
        "text/csv"
    )

except Exception as e:

    st.error(f"Error : {e}")