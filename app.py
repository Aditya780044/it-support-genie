import streamlit as st
import os

from predictor import get_response
from database import create_database, save_query

# ------------------------------------------------
# Page Config
# ------------------------------------------------

st.set_page_config(
    page_title="IT Support Genie",
    page_icon="🤖",
    layout="wide"
)

create_database()

# ------------------------------------------------
# Title
# ------------------------------------------------

st.title("🤖 AI IT Support Genie")
st.caption("IT Support & SOP Recommendation System")

st.markdown("---")

# ------------------------------------------------
# Session State
# ------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------
# Display Previous Messages
# ------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------------------------
# Chat Input
# ------------------------------------------------

user_input = st.chat_input("Type your IT issue here...")

if user_input:

    # Show User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI Response

    category, answer, steps, sop, confidence = get_response(user_input)

    # --------------------------------------------
    # Greeting Response
    # --------------------------------------------

    if category == "Greeting":

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    else:

        # Save Query

        save_query(
            user_input,
            category,
            round(confidence, 2),
            sop
        )

        # Build Response

        response = f"""
### 📌 Issue Category

**{category}**

---

### 💡 Solution

{answer}

---

### 🔧 Troubleshooting Steps

"""

        for step in steps:

            if step.strip():
                response += f"- {step.strip()}\n"

        # SOP

        if sop:

            response += f"""

---

### 📄 Recommended SOP

{sop}

"""

        # Display Assistant

        with st.chat_message("assistant"):

            st.markdown(response)

            # SOP Download

            if sop:

                sop_path = os.path.join("sops", sop)

                if os.path.isfile(sop_path):

                    with open(sop_path, "rb") as file:

                        st.download_button(
                            "📥 Download SOP",
                            file,
                            file_name=sop
                        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

# ------------------------------------------------
# Sidebar
# ------------------------------------------------

with st.sidebar:

    st.header("📌 About")

    st.write(
        """
AI IT Support Genie is an intelligent chatbot that helps users resolve common IT issues and recommends troubleshooting steps and SOP documents.
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
        "Microsoft 365",
        "Security",
        "Software"
    ]

    for item in categories:
        st.write("✅", item)

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# ------------------------------------------------
# Footer
# ------------------------------------------------

st.markdown("---")

st.caption("© 2026 AI IT Support Genie | BITS Pilani Dissertation Project")