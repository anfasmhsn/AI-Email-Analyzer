import streamlit as st
from chatbot.chat import ask_chatbot
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from classifier import classify_email
from sentiment import get_sentiment
from priority import get_priority
from database import get_emails, delete_selected
from gmail_fetch import fetch_emails
from database import save_email


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SmartMail AI",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)
if "page" not in st.session_state:
    st.session_state.page = "Inbox"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main dashboard spacing — FIXED */
    .block-container {
        padding-top: 3rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        width: 230px !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    /* Main title */
    .smartmail-title {
        font-size: 30px;
        font-weight: 700;
        margin-top: 0.5rem;
        margin-bottom: 5px;
    }

    .smartmail-subtitle {
        color: #888;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Top search area */
    .search-box {
        background: #202124;
        border-radius: 25px;
        padding: 8px 18px;
    }

    /* Statistics */
    .stat-card {
        background: #202124;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .stat-title {
        font-size: 13px;
        color: #aaa;
    }

    .stat-value {
        font-size: 25px;
        font-weight: 600;
    }

    /* Email detail */
    .email-detail {
        background: #202124;
        border-radius: 12px;
        padding: 25px;
        margin-top: 20px;
    }

    .email-subject {
        font-size: 23px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .email-meta {
        color: #aaa;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .email-body {
        background: #18191f;
        border-radius: 8px;
        padding: 20px;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 8px;
    }

    /* Divider */
    .divider {
        margin-top: 10px;
        margin-bottom: 10px;
        border-bottom: 1px solid #333;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📧 SmartMail AI")
    st.caption("AI-powered email management")

    st.divider()

    # -----------------------------------------------------
    # IMPORT GMAIL
    # -----------------------------------------------------

    if st.button(
        "📥  Import Gmail",
        use_container_width=True
    ):

        with st.spinner("Importing Gmail emails..."):

            emails = fetch_emails()

            imported_count = 0

            for mail in emails:

                text = (
                    mail.get("subject", "")
                    + " "
                    + mail.get("body", "")
                )

                category = classify_email(text)
                sentiment = get_sentiment(text)
                priority = get_priority(
                    text,
                    category,
                    sentiment
                )

                save_email(
                    mail.get("gmail_id", ""),
                    mail.get("sender", ""),
                    mail.get("subject", ""),
                    mail.get("body", ""),
                    category,
                    sentiment,
                    priority,
                    mail.get("date", ""),
                    ",".join(mail.get("labels", []))
                )

                imported_count += 1

        st.success(
            f"{imported_count} emails imported!"
        )

        st.rerun()

    st.divider()
    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    st.markdown("### 📬 Mail")

    if st.button("📥 Inbox", use_container_width=True):
        st.session_state.page = "Inbox"
        st.rerun()

    if st.button("🔥 High Priority", use_container_width=True):
        st.session_state.page = "High Priority"
        st.rerun()

    if st.button("⭐ Starred", use_container_width=True):
        st.session_state.page = "Starred"
        st.rerun()

    if st.button("📤 Sent", use_container_width=True):
        st.session_state.page = "Sent"
        st.rerun()

    if st.button("📝 Drafts", use_container_width=True):
        st.session_state.page = "Drafts"
        st.rerun()
    # -----------------------------------------------------
    # MANUAL EMAIL ANALYSIS
    # -----------------------------------------------------

    st.markdown("### 🤖 AI Tools")

    analyze_mode = st.checkbox(
        "Analyze Email"
    )

    st.divider()

    st.caption("SmartMail AI")
    st.caption("Email Intelligence Dashboard")


# =========================================================
# LOAD EMAILS
# =========================================================

emails = get_emails()

df = pd.DataFrame(
    emails,
    columns=[
        "id",
        "gmail_id",
        "sender",
        "subject",
        "body",
        "category",
        "sentiment",
        "priority",
        "date",
        "labels"
    ]
)


# =========================================================
# MAIN HEADER
# =========================================================

header_col1, header_col2 = st.columns(
    [3, 1]
)

with header_col1:

    st.markdown(
        '<div class="smartmail-title">📧 SmartMail AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="smartmail-subtitle">'
        'Smart email classification and management'
        '</div>',
        unsafe_allow_html=True
    )


with header_col2:

    st.write("")

    if st.button(
        "🔄 Refresh",
        use_container_width=True
    ):
        st.rerun()


# =========================================================
# MANUAL AI ANALYSIS
# =========================================================

if analyze_mode:

    st.markdown("### 🤖 Analyze Email")

    email_text = st.text_area(
        "Paste email content",
        height=130,
        placeholder="Enter email text here..."
    )

    if st.button("Analyze", type="primary"):

        if email_text.strip():

            category = classify_email(
                email_text
            )

            sentiment = get_sentiment(
                email_text
            )

            priority = get_priority(
                email_text,
                category,
                sentiment
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "📂 Category",
                category
            )

            c2.metric(
                "💭 Sentiment",
                sentiment
            )

            c3.metric(
                "🔥 Priority",
                priority
            )

        else:

            st.warning(
                "Please enter an email."
            )


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

total_emails = len(df)

high_priority = len(
    df[df["priority"] == "High"]
)

category_count = (
    df["category"].nunique()
    if not df.empty
    else 0
)

if not df.empty:

    top_sender = (
        df["sender"]
        .value_counts()
        .idxmax()
    )

else:

    top_sender = "N/A"


st.markdown("### 📊 Overview")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "📧 Emails",
        total_emails
    )


with c2:

    st.metric(
        "🔥 High Priority",
        high_priority
    )


with c3:

    st.metric(
        "📂 Categories",
        category_count
    )


with c4:

    st.metric(
        "👤 Top Sender",
        top_sender
    )


# =========================================================
# SEARCH + FILTER
# =========================================================

search_col, filter_col = st.columns(
    [4, 1]
)


with search_col:

    search = st.text_input(
        "🔍 Search emails",
        placeholder="Search sender or subject..."
    )


with filter_col:

    categories = (
        ["All"]
        + sorted(df["category"].dropna().unique().tolist())
        if not df.empty
        else ["All"]
    )

    selected_category = st.selectbox(
        "Category",
        categories
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


if search:

    filtered_df = filtered_df[
        filtered_df["sender"]
        .str.contains(
            search,
            case=False,
            na=False
        )
        |
        filtered_df["subject"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["category"]
        == selected_category
    ]
# =========================================================
# SIDEBAR PAGE FILTER
# =========================================================

if st.session_state.page == "High Priority":

    filtered_df = filtered_df[
        filtered_df["priority"] == "High"
    ]

elif st.session_state.page == "Starred":

    # Starred support will be added later
    filtered_df = filtered_df.iloc[0:0]

elif st.session_state.page == "Sent":

    # Sent support will be added later
    filtered_df = filtered_df.iloc[0:0]

elif st.session_state.page == "Drafts":

    # Draft support will be added later
    filtered_df = filtered_df.iloc[0:0]

elif st.session_state.page == "Inbox":

    # Show all imported emails
    filtered_df = filtered_df

# =========================================================
# PRIORITY SORT
# =========================================================

priority_order = {
    "High": 0,
    "Medium": 1,
    "Low": 2
}

filtered_df["priority_order"] = (
    filtered_df["priority"]
    .map(priority_order)
)

filtered_df = filtered_df.sort_values(
    "priority_order"
)


# =========================================================
# EMAIL LIST
# =========================================================

st.markdown("### 📬 Emails")


# Only show useful columns
display_df = filtered_df[
    [
        "id",
        "sender",
        "subject",
        "category",
        "sentiment",
        "priority",
        "date"
    ]
].copy()


# Shorten long sender names
display_df["sender"] = (
    display_df["sender"]
    .astype(str)
    .str.slice(0, 35)
)


# Shorten subjects
display_df["subject"] = (
    display_df["subject"]
    .astype(str)
    .str.slice(0, 80)
)

# =========================================================
# AGGRID
# =========================================================

gb = GridOptionsBuilder.from_dataframe(
    display_df
)

gb.configure_default_column(
    editable=False,
    sortable=True,
    filterable=True,
    resizable=True
)

# Allow checkbox + row selection
gb.configure_selection(
    "multiple",
    use_checkbox=True,
    pre_selected_rows=[]
)

gb.configure_grid_options(
    rowSelection="multiple",
    suppressRowClickSelection=False,
    animateRows=True
)

# Column widths
gb.configure_column(
    "id",
    hide=True
)

gb.configure_column(
    "sender",
    header_name="Sender",
    width=180
)

gb.configure_column(
    "subject",
    header_name="Subject",
    width=400
)

gb.configure_column(
    "category",
    header_name="Category",
    width=180
)

gb.configure_column(
    "sentiment",
    header_name="Sentiment",
    width=120
)

gb.configure_column(
    "priority",
    header_name="Priority",
    width=120
)

gb.configure_column(
    "date",
    header_name="Date",
    width=160
)

grid = AgGrid(
    display_df,
    gridOptions=gb.build(),
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    enable_enterprise_modules=False,
    height=550,
    fit_columns_on_grid_load=False,
    theme="streamlit"
)


# =========================================================
# SELECTED EMAIL
# =========================================================

selected = grid["selected_rows"]


# =========================================================
# ACTION BUTTONS
# =========================================================

action1, action2, action3 = st.columns([1, 1, 4])


# ---------------------------------------------------------
# OPEN EMAIL
# ---------------------------------------------------------

with action1:

    if st.button(
        "📖 Open Email",
        use_container_width=True
    ):

        if selected is None:

            st.warning("Select an email first.")

        elif isinstance(selected, pd.DataFrame):

            if selected.empty:

                st.warning("Select an email first.")

            else:

                email_id = int(
                    selected.iloc[0]["id"]
                )

                st.session_state["opened_email"] = email_id

                st.rerun()

        elif isinstance(selected, list):

            if len(selected) == 0:

                st.warning("Select an email first.")

            else:

                email_id = int(
                    selected[0]["id"]
                )

                st.session_state["opened_email"] = email_id

                st.rerun()


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------

with action2:

    if st.button(
        "🗑 Delete",
        use_container_width=True
    ):

        if selected is None:

            st.warning("Select email(s) first.")

        elif isinstance(selected, pd.DataFrame):

            if selected.empty:

                st.warning("Select email(s) first.")

            else:

                ids = selected["id"].astype(int).tolist()

                delete_selected(ids)

                st.success(
                    "Selected emails deleted."
                )

                st.rerun()

        elif isinstance(selected, list):

            if len(selected) == 0:

                st.warning("Select email(s) first.")

            else:

                ids = [
                    int(row["id"])
                    for row in selected
                ]

                delete_selected(ids)

                st.success(
                    "Selected emails deleted."
                )

                st.rerun()

# =========================================================
# OPENED EMAIL
# =========================================================

if "opened_email" in st.session_state:

    opened_id = st.session_state[
        "opened_email"
    ]

    email_rows = df[
        df["id"] == opened_id
    ]

    if not email_rows.empty:

        mail = email_rows.iloc[0]

        st.divider()

        top1, top2 = st.columns(
            [5, 1]
        )

        with top1:

            st.markdown(
                "### 📩 Email"
            )

        with top2:

            if st.button(
                "✖ Close",
                use_container_width=True
            ):

                del st.session_state[
                    "opened_email"
                ]

                st.rerun()


        st.markdown(
            f"## {mail['subject']}"
        )

        st.markdown(
            f"""
            **From:** {mail['sender']}  
            **Date:** {mail['date']}  
            **Category:** `{mail['category']}`  
            **Sentiment:** `{mail['sentiment']}`  
            **Priority:** `{mail['priority']}`
            """
        )

        st.divider()

        st.markdown(
            "### Message"
        )

        st.markdown(
            f"""
            <div class="email-body">
            {mail['body']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🗑 Delete This Email",
            type="secondary"
        ):

            delete_selected(
                [int(mail["id"])]
            )

            del st.session_state[
                "opened_email"
            ]

            st.success(
                "Email deleted."
            )

            st.rerun()


# =========================================================
# ANALYTICS
# =========================================================

st.divider()

chart1, chart2 = st.columns(2)


with chart1:

    st.subheader(
        "📂 Category Distribution"
    )

    if not df.empty:

        category_counts = (
            df["category"]
            .value_counts()
        )

        st.bar_chart(
            category_counts
        )


with chart2:

    st.subheader(
        "🔥 Priority Distribution"
    )

    if not df.empty:

        priority_counts = (
            df["priority"]
            .value_counts()
            .reindex(
                ["High", "Medium", "Low"]
            )
            .fillna(0)
        )

        st.bar_chart(
            priority_counts
        )


# =========================================================
# DOWNLOAD REPORT
# =========================================================

if not filtered_df.empty:

    download_df = filtered_df.drop(
        columns=["priority_order"],
        errors="ignore"
    )

    csv = download_df.to_csv(
        index=False
    )

    st.download_button(
        "📥 Download Email Report",
        csv,
        "smartmail_report.csv",
        "text/csv"
    )
# ==========================================
# FLOATING SMARTMAIL AI CHATBOT
# ==========================================

st.markdown("""
<style>
/* Floating chatbot button */
div.stButton > button[kind="secondary"] {
    border-radius: 50%;
}

/* Chat panel */
.chatbot-panel {
    position: fixed;
    right: 24px;
    bottom: 100px;
    width: 350px;
    max-width: calc(100vw - 40px);
    height: 480px;
    max-height: 70vh;
    background: #111827;
    border: 1px solid #374151;
    border-radius: 18px;
    padding: 16px;
    z-index: 999;
    color: white;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}
</style>
""", unsafe_allow_html=True)

# Initialize chatbot state
if "chatbot_open" not in st.session_state:
    st.session_state.chatbot_open = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Floating bot button
st.markdown("""
<style>
div[data-testid="stVerticalBlock"]:has(.bot-anchor) {
    position: relative;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bot-anchor"></div>', unsafe_allow_html=True)

button_col1, button_col2 = st.columns([9, 1])

with button_col2:
    if st.button(
        "🤖",
        key="floating_chatbot_button",
        help="Chat with SmartMail AI"
    ):
        st.session_state.chatbot_open = (
            not st.session_state.chatbot_open
        )

# Chat panel
if st.session_state.chatbot_open:

    with st.container(border=True):

        header_col1, header_col2 = st.columns([5, 1])

        with header_col1:
            st.subheader("🤖 SmartMail AI")
            st.caption("Your intelligent email assistant")

        with header_col2:
            if st.button("✕", key="close_chatbot"):
                st.session_state.chatbot_open = False
                st.rerun()

        st.divider()

        # Welcome message
        if not st.session_state.chat_messages:
            st.info(
                "Hi! 👋 Ask me about your emails, "
                "salary messages, job opportunities, "
                "or high-priority emails."
            )

        # Display chat history
        for message in st.session_state.chat_messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        question = st.chat_input(
            "Ask anything about your emails...",
            key="smartmail_chat_input"
        )

        if question:

            st.session_state.chat_messages.append({
                "role": "user",
                "content": question
            })

            with st.spinner("Searching your emails..."):

                try:
                    answer = ask_chatbot(question)

                except Exception as error:
                    answer = (
                        "Sorry, I couldn't process your question. "
                        f"Error: {error}"
                    )

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": answer
            })

            st.rerun()    
# ============================================
# SMARTMAIL AI — FLOATING CHATBOT
# ============================================

import streamlit as st
from chatbot.chat import ask_chatbot

# Initialize chatbot state
if "chatbot_open" not in st.session_state:
    st.session_state.chatbot_open = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# Floating chatbot styling
st.markdown("""
<style>

/* Floating launcher container */
.st-key-smartmail_chat_launcher {
    position: fixed !important;
    right: 28px !important;
    bottom: 28px !important;
    width: 72px !important;
    z-index: 999999 !important;
}

/* Large circular robot button */
/* Floating SmartMail AI button */
.st-key-smartmail_chat_launcher {
    position: fixed !important;
    right: 28px !important;
    bottom: 28px !important;
    width: 76px !important;
    z-index: 999999 !important;
}

.st-key-smartmail_chat_launcher button {
    width: 72px !important;
    height: 72px !important;
    min-height: 72px !important;
    padding: 0 !important;

    border-radius: 50% !important;
    border: 2px solid #93c5fd !important;

    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    ) !important;

    box-shadow:
        0 0 15px rgba(59, 130, 246, 0.55),
        0 5px 25px rgba(0, 0, 0, 0.4) !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    transition: all 0.25s ease !important;
}

/* Enlarge the actual icon inside the button */
.st-key-smartmail_chat_launcher button p {
    font-size: 36px !important;
    line-height: 1 !important;
    margin: 0 !important;
}

.st-key-smartmail_chat_launcher button:hover {
    transform: scale(1.08) !important;
    border-color: #c4b5fd !important;
    box-shadow: 0 0 24px rgba(124, 58, 237, 0.8) !important;
}
    transition: transform 0.2s ease,
                box-shadow 0.2s ease !important;
}

/* Hover effect */
.st-key-smartmail_chat_launcher button:hover {
    transform: scale(1.08) !important;
    box-shadow:
        0 0 20px rgba(124, 58, 237, 0.75),
        0 5px 24px rgba(0, 0, 0, 0.4) !important;
    border-color: #c4b5fd !important;
}

/* Floating chat panel */
.st-key-smartmail_chat_panel {
    position: fixed !important;
    right: 24px !important;
    bottom: 108px !important;
    width: 390px !important;
    max-width: calc(100vw - 32px) !important;
    max-height: 70vh !important;
    overflow-y: auto !important;
    z-index: 999998 !important;
    background: #101522 !important;
    border: 1px solid #35415b !important;
    border-radius: 20px !important;
    padding: 18px !important;
    box-shadow: 0 12px 45px rgba(0, 0, 0, 0.55) !important;
}

/* Chat panel headings */
.st-key-smartmail_chat_panel h3 {
    color: #ffffff !important;
    font-size: 21px !important;
}

/* Chat panel buttons */
.st-key-smartmail_chat_panel button {
    border-radius: 10px !important;
}

/* Input field */
.st-key-smartmail_chat_panel input {
    border-radius: 12px !important;
}

/* Small screens */
@media (max-width: 480px) {
    .st-key-smartmail_chat_panel {
        right: 12px !important;
        bottom: 94px !important;
        width: calc(100vw - 24px) !important;
        max-width: calc(100vw - 24px) !important;
    }

    .st-key-smartmail_chat_launcher {
        right: 18px !important;
        bottom: 18px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================
# FLOATING CHAT PANEL
# ============================================

if st.session_state.chatbot_open:

    with st.container(key="smartmail_chat_panel"):

        header_col, close_col = st.columns([5, 1])

        with header_col:
            st.markdown("### 🤖 SmartMail AI")
            st.caption("Your intelligent email assistant")

        with close_col:
            if st.button("✕", key="smartmail_close"):
                st.session_state.chatbot_open = False
                st.rerun()

        st.divider()

        # Suggested questions
        if not st.session_state.chat_messages:

            st.markdown("**Hi there! 👋**")
            st.write("How can I help you with your emails?")

            suggestions = [
                "Show high-priority emails",
                "Find emails about salary",
                "Summarize recent emails",
            ]

            for index, suggestion in enumerate(suggestions):

                if st.button(
                    suggestion,
                    key=f"smartmail_suggestion_{index}",
                    use_container_width=True
                ):
                    st.session_state.pending_chat_question = suggestion
                    st.rerun()

        # Conversation history
        for message in st.session_state.chat_messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input form
        with st.form(
            "smartmail_chat_form",
            clear_on_submit=True
        ):

            question = st.text_input(
                "Ask SmartMail AI",
                placeholder="Ask anything about your emails...",
                label_visibility="collapsed"
            )

            submitted = st.form_submit_button(
                "Send ➤",
                use_container_width=True
            )

        # Handle submitted message
        pending_question = st.session_state.pop(
            "pending_chat_question",
            ""
        )

        user_question = (
            question.strip()
            if submitted and question.strip()
            else pending_question
        )

        if user_question:

            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_question
            })

            with st.spinner("Searching your emails..."):

                try:
                    answer = ask_chatbot(user_question)

                except Exception:
                    answer = (
                        "Sorry, I couldn't process your request. "
                        "Please try again."
                    )

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": answer
            })

            st.rerun()


# ============================================
# FLOATING ROBOT BUTTON
# ============================================

with st.container(key="smartmail_chat_launcher"):

    if st.button(
        "🤖",
        key="smartmail_open_chat",
        help="Chat with SmartMail AI"
    ):
        st.session_state.chatbot_open = (
            not st.session_state.chatbot_open
        )
        st.rerun()
