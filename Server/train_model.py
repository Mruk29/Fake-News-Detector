import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

# Load true and fake datasets
true_df = pd.read_csv("data/True.csv")
fake_df = pd.read_csv("data/Fake.csv")

# Add a label column
true_df['label'] = 1  # Real
fake_df['label'] = 0  # Fake

# Combine them
df = pd.concat([true_df, fake_df], axis=0)
df = df[['text', 'label']]  # Use only text and label columns
df = df.sample(frac=1).reset_index(drop=True)  # Shuffle

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'], test_size=0.2, random_state=42
)

# TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_tfidf = tfidf.fit_transform(X_train)

# Train logistic regression model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Save model and vectorizer
os.makedirs("model", exist_ok=True)

with open("model/fake_news_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

print("✅ Model and vectorizer saved in 'server/model/'")
