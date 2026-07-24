import streamlit as st
import os

from predictor import get_response
from database import create_database, save_query

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="IT Support Genie",
    page_icon="🤖",
    layout="wide"
)

create_database()

# -----------------------------
# Title
# -----------------------------

st.title("🤖 AI IT Support Genie")
st.caption("IT Support & SOP Recommendation System")

st.markdown("---")

# -----------------------------
# Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Chat
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------

user_input = st.chat_input("Type your IT issue here...")

if user_input:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get Prediction

    category, answer, steps, sop, confidence = get_response(user_input)

    # Save in Database

    save_query(
        user_input,
        category,
        round(confidence, 2),
        sop
    )

    # Build Response

    response = f"""
### 📌 Category

{category}

---

### 💡 Solution

{answer}

---

### 🔧 Troubleshooting Steps

"""

    for step in steps:

        response += f"- {step}\n"

    response += "\n---\n"

    response += f"### 📄 Recommended SOP\n\n{sop}\n\n"

    # Confidence removed
    # Display Bot Response

    with st.chat_message("assistant"):

        st.markdown(response)

        # Download SOP

        sop_path = os.path.join("sops", sop)

        if os.path.exists(sop_path):

            with open(sop_path, "rb") as file:

                st.download_button(
                    "📥 Download SOP",
                    file,
                    file_name=sop
                )

        else:

            st.info("SOP file not available.")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
    # -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("📌 About")

    st.write(
        """
        **AI IT Support Genie**

        This chatbot helps users solve common IT issues by
        recommending troubleshooting steps and SOP documents.
        """
    )

    st.markdown("---")

    st.subheader("Supported Categories")

    categories = [
        "VPN",
        "Outlook",
        "Printer",
        "WiFi",
        "Account",
        "Performance",
        "Citrix",
        "M365",
        "Security",
        "Software"
    ]

    for item in categories:
        st.write("✅", item)

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# -----------------------------
# Footer
# -----------------------------

st.markdown("---")

st.caption(
    "© 2026 AI IT Support Genie | BITS Pilani Dissertation Project"
)