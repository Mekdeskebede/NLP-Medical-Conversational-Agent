import json
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import nltk

def process_user_input(user_input):
    # Load intents from a JSON file
    with open('/kaggle/input/amharic-data/amharic_intent.json', 'r') as file:
        intents = json.load(file)

    # Prepare the training data for intent recognition
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
    train_features = vectorizer.fit_transform(train_texts)

    # Train a logistic regression model for intent recognition
    intent_classifier = LogisticRegression()
    intent_classifier.fit(train_features, train_labels)

    predicted_intent = None

    try:
        single_words = ["እርዳኝ", "እገዛ", "ቆንጆ", "እሺ", "አመሰግናለሁ", "cao", "ደህና", "cya", "ሰላምታ", "ሰላም", "ሃይ", "ሄይ", "ሄሎ"]
        # Check if the user input is in Amharic (except for the word 'cya')
        is_amharic = all("\u1200" <= c <= "\u137F" or c.isspace() or c in ",/?!" for c in user_input) and "cya" not in user_input.lower()

        # Check if the user input is a single word and request more context if so
        if not is_amharic:
            filtered_response = "እባክዎን ጥያቄዎን በአማርኛ ቋንቋ ብቻ ያቅርቡ"
        elif len(user_input.split()) <= 1 and user_input not in single_words:
            filtered_response = np.random.choice(["የእርስዎ ግብዓት በጣም አጭር ነው። እባክዎ ተጨማሪ አውድ ወይም የተሟላ ዓረፍተ ነገር ያቅርቡ።",
                                                  "ይቅርታ፣ አልገባኝም። እባክህ እንደገና መግለጽ ትችላለህ ወይስ ሌላ ጥያቄ ጠይቅ?",
                                                  "አሁንም እየተማርኩ ነው። ተጨማሪ ዝርዝሮችን መስጠት ትችላለህ ወይም ሌላ ጥያቄ መሞከር ትችላለህ?"])
    
        else:
            # Convert the user input into a numerical representation
            user_input_features = vectorizer.transform([user_input])

            # Predict the intent for the user input
            predicted_intent = intent_classifier.predict(user_input_features)[0]

            # Check if the predicted intent matches any known intents
            if predicted_intent not in intent_responses:
                predicted_intent = None

            # Generate response based on the predicted intent
            if predicted_intent is not None:
                response = intent_responses.get(predicted_intent)
                filtered_response = np.random.choice(response)
            else:
                filtered_response = "I'm sorry, I couldn't understand your request."

        return user_input, predicted_intent, filtered_response

    except Exception as e:
        filtered_response = "An error occurred while processing your request: {}".format(str(e))
        return user_input, predicted_intent, filtered_response

# Start a conversation loop
while True:
    user_input = input("User: ")
    user_input,predicted_intent, filtered_response = process_user_input(user_input)
    print("Assistant:", filtered_response)

    # Exit the loop if the user enters 'exit' or 'quit'
    if user_input.lower() in ['በቃ', 'quit']:
        print("Assistant:", "ቻው ቻው")
        break