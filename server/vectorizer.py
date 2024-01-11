from sklearn.feature_extraction.text import CountVectorizer
import json
import sys

# Read the training texts from the JSON file
with open("../data/amharic_intent.json") as file:
    intents = json.load(file)
train_texts = []
train_labels = []
intent_responses = {}  # Dictionary to store tag-to-response mapping
for intent in intents:
    tag = intent['tag']
    patterns = intent['patterns']
    response = intent['responses']
    intent_responses[tag] = response  # Add tag-to-response mapping
    for pattern in patterns:
        # Tokenize pattern
        tokens = nltk.word_tokenize(pattern)

        # Join tokens back into a string
        processed_pattern = " ".join(tokens)

        train_texts.append(processed_pattern)
        train_labels.append(tag)

# Feature extraction using bag-of-words with n-grams
vectorizer = CountVectorizer(lowercase=True, token_pattern=r'\b\w+\b', ngram_range=(1, 2))
trainFeatures = vectorizer.fit_transform(train_texts)

# Fit and transform the training texts
# trainFeatures = vectorizer.fit_transform(trainTexts)

# Convert the vectorized features to a JSON-compatible format
featuresJson = trainFeatures.toarray().tolist()

# Print the vectorized features as JSON
print(json.dumps(featuresJson))