# ==========================================
# AI IT Support Genie
# NLP Engine
# Deep Learning using Sentence Embeddings
# ==========================================

import os
import joblib
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer

print("=" * 50)
print(" AI IT SUPPORT GENIE - NLP ENGINE")
print("=" * 50)

# -----------------------------
# Load Knowledge Base
# -----------------------------

print("\nLoading Knowledge Base...")

df = pd.read_excel("data/knowledge_base.xlsx")

required_columns = ["query", "category", "answer", "steps"]

for col in required_columns:
    if col not in df.columns:
        raise Exception(f"Missing column: {col}")

print(f"Knowledge Base Loaded Successfully")
print(f"Total Records : {len(df)}")

# -----------------------------
# Load Embedding Model
# -----------------------------

print("\nLoading Sentence Transformer Model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded Successfully")

# -----------------------------
# Create Embeddings
# -----------------------------

print("\nGenerating Sentence Embeddings...")

embeddings = embedding_model.encode(
    df["query"].tolist(),
    convert_to_numpy=True,
    show_progress_bar=True
)

print("Embeddings Generated Successfully")

# -----------------------------
# Create Models Folder
# -----------------------------

os.makedirs("models", exist_ok=True)

# -----------------------------
# Save Embeddings
# -----------------------------

np.save("models/query_embeddings.npy", embeddings)

# -----------------------------
# Save Knowledge Base
# -----------------------------

joblib.dump(
    df,
    "models/knowledge_base.pkl"
)

# -----------------------------
# Save Sentence Transformer
# -----------------------------

embedding_model.save("models/embedding_model")

print("\nSaving Files...")

print("✓ query_embeddings.npy")
print("✓ knowledge_base.pkl")
print("✓ embedding_model")

print("\n========================================")
print(" NLP ENGINE COMPLETED SUCCESSFULLY ")
print("========================================")