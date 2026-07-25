# ==========================================
# AI IT Support Genie
# Predictor
# ==========================================

from textblob import TextBlob
import joblib
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------------------
# Load Models
# ------------------------------------------

knowledge_base = joblib.load("models/knowledge_base.pkl")

embedding_model = SentenceTransformer("models/embedding_model")

query_embeddings = np.load("models/query_embeddings.npy")

sop_df = pd.read_excel("data/sop_mapping.xlsx")

# ------------------------------------------
# Greetings
# ------------------------------------------

GREETINGS = [
    "hi",
    "hello",
    "hey",
    "hii",
    "good morning",
    "good afternoon",
    "good evening",
    "good night"
]

# Similarity Threshold

THRESHOLD = 0.60


# ==========================================
# Prediction Function
# ==========================================

def get_response(user_query):

    # -----------------------------
    # Safety
    # -----------------------------

    user_query = str(user_query).strip()

    if user_query == "":
        return (
            "Unknown",
            "Please enter your IT issue.",
            [],
            "",
            0.0
        )

    query = user_query.lower()

    # -----------------------------
    # Greeting
    # -----------------------------

    if query in GREETINGS:

        return (
            "Greeting",
            "Hello 👋 Welcome to IT Support Genie. How can I help you today?",
            [],
            "",
            1.0
        )

    # -----------------------------
    # Spell Correction
    # -----------------------------

    corrected_query = str(TextBlob(user_query).correct())

    # -----------------------------
    # Generate Embedding
    # -----------------------------

    user_embedding = embedding_model.encode([corrected_query])

    # -----------------------------
    # Similarity Search
    # -----------------------------

    similarity = cosine_similarity(
        user_embedding,
        query_embeddings
    )

    best_index = np.argmax(similarity)

    confidence = float(similarity[0][best_index])

    # -----------------------------
    # Unknown Issue Detection
    # -----------------------------

    if confidence < THRESHOLD:

        return (
            "Unknown",
            """👋 Hello!

Thank you for contacting AI IT Support Genie.

Unfortunately, I couldn't find a matching solution for your issue in the current knowledge base.

📞 Please contact the IT Helpdesk for further assistance.

Your issue may require manual investigation by the support team.
""",
            [],
            "",
            confidence
        )

    # -----------------------------
    # Best Match
    # -----------------------------

    row = knowledge_base.iloc[best_index]

    category = row["category"]
    answer = row["answer"]

    # -----------------------------
    # Troubleshooting Steps
    # -----------------------------

    steps_text = str(row["steps"])

    steps = [
        step.strip()
        for step in steps_text.split(".")
        if step.strip()
    ]

    # -----------------------------
    # SOP Mapping
    # -----------------------------

    sop = ""

    match = sop_df[sop_df["category"] == category]

    if not match.empty:
        sop = match.iloc[0]["sop_filename"]

    # -----------------------------
    # Return Result
    # -----------------------------

    return (
        category,
        answer,
        steps,
        sop,
        confidence
    )