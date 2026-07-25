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

# ------------------------------------------------
# Custom Header
# ------------------------------------------------

st.markdown("""
<h1 style='text-align:center;color:#1E88E5;'>
🤖 AI IT Support Genie
</h1>
""", unsafe_allow_html=True)

st.markdown(
"""
<div style='
padding:20px;
border-radius:12px;
background-color:#F5F7FA;
border:1px solid #D3D3D3;'>

<h4>Welcome to AI IT Support Genie 👋</h4>


<b>How may i help you:</b>


</div>
""",
unsafe_allow_html=True
)

st.write("")

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
## 🔹 {category}

### 💡 Solution

{answer}

### 🛠 Troubleshooting

"""

        # Format troubleshooting steps

        formatted_steps = []

        i = 0

        while i < len(steps):

            current = steps[i].strip()

            if current.isdigit() and i + 1 < len(steps):

                formatted_steps.append(f"{current} - {steps[i + 1].strip()}")

                i += 2

            else:

                if current:

                    formatted_steps.append(current)

                i += 1

        for step in formatted_steps:

            response += f"{step}\n"

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

            # Download SOP

            if sop:

                sop_path = os.path.join("sops", sop)

                if os.path.isfile(sop_path):

                    with open(sop_path, "rb") as file:

                       st.download_button(
    label="📥 Download SOP",
    data=file.read(),
    file_name=sop,
    mime="application/pdf",
    key=f"sop_{sop}"
)

        # Save assistant message

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

    st.image("assets/chatbot.png", width=70)

    st.title("IT Support Genie")

    st.caption("Version 2.0")

    st.write("BITS Pilani Dissertation Project")

    st.markdown("---")

    if st.button(
        "🗑 Clear Chat",
        key="clear_chat"
    ):

        st.session_state.messages = []

        st.rerun()
# ------------------------------------------------
# Footer
# ------------------------------------------------

st.markdown("---")

st.caption("© 2026 AI IT Support Genie | BITS Pilani Dissertation Project")