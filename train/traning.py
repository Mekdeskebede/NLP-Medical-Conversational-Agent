import json
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Load intents from a JSON file
with open('/kaggle/input/amharic-data/amharic_intent.json', 'r') as file:
    intents = json.load(file)

# Prepare the training data for intent recognition
train_texts = []
train_labels = []
for intent in intents:
    tag = intent['tag']
    patterns = intent['patterns']
    for pattern in patterns:
        train_texts.append(pattern)
        train_labels.append(tag)

# Feature extraction using bag-of-words with n-grams
vectorizer = CountVectorizer(lowercase=True, token_pattern=r'\b\w+\b', ngram_range=(1, 2))
train_features = vectorizer.fit_transform(train_texts)

# Train a logistic regression model for intent recognition
intent_classifier = LogisticRegression()
intent_classifier.fit(train_features, train_labels)

# User input
user_input = "cya"

# Convert the user input into a numerical representation
user_input_features = vectorizer.transform([user_input])

# Predict the intent for the user input
predicted_intent = intent_classifier.predict(user_input_features)[0]

print("User input:", user_input)
print("Predicted intent:", predicted_intent)