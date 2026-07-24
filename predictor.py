# ==========================================
# AI IT Support Genie
# Predictor
# ==========================================

import joblib
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load Knowledge Base
knowledge_base = joblib.load("models/knowledge_base.pkl")

# Load Embedding Model
embedding_model = SentenceTransformer("models/embedding_model")

# Load Query Embeddings
query_embeddings = np.load("models/query_embeddings.npy")

# Load SOP Mapping
sop_df = pd.read_excel("data/sop_mapping.xlsx")

# Greetings
GREETINGS = [
    "hi",
    "hello",
    "hey",
    "hii",
    "good morning",
    "good afternoon",
    "good evening"
]


def get_response(user_query):

    query = user_query.strip().lower()

    # Greeting
    if query in GREETINGS:
        return (
            "Greeting",
            "Hello 👋 Welcome to IT Support Genie. How can I help you today?",
            [],
            "",
            1.0
        )

    # Create embedding
    user_embedding = embedding_model.encode([user_query])

    # Calculate similarity
    similarity = cosine_similarity(user_embedding, query_embeddings)

    # Best Match
    best_index = np.argmax(similarity)

    confidence = float(similarity[0][best_index])

    row = knowledge_base.iloc[best_index]

    category = row["category"]
    answer = row["answer"]

    # Steps
    steps_text = str(row["steps"])

    steps = [
        step.strip()
        for step in steps_text.split(".")
        if step.strip()
    ]

    # SOP
    sop = ""

    match = sop_df[sop_df["category"] == category]

    if not match.empty:
        sop = match.iloc[0]["sop_filename"]

    return (
        category,
        answer,
        steps,
        sop,
        confidence
    )