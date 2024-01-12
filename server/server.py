from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
nltk.download('punkt')
import json
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

prefixes = ['በ', 'የ', 'ለ',]
suffixes = ["ነ", "ን", "ው", "ል", "ም", "ት", "ላ", "ምን", "ለት","ሁ"]

# Function to remove prefixes from an Amharic word
def remove_prefix(word):
    for prefix in prefixes:
        if word.startswith(prefix):
            return word[len(prefix):]
    # for suffix in suffixes:
    #         if word.endswith(suffix):
    #             word = word[:-len(suffix)]
    return word
def process_user_input(user_input, intent_classifier, vectorizer, intent_responses):
    try:
        predicted_intent = None
        single_words = ["እርዳኝ", "እገዛ", "ቆንጆ", "እሺ", "አመሰግናለሁ", "ደህና", "ሰላምታ", "ሰላም", "ሃይ", "ሄይ", "ሄሎ", "መልካም", "ማን ልበልህ"]
        # Check if the user input is in Amharic (except for the word 'cya')
        is_amharic = all("\u1200" <= c <= "\u137F" or c.isspace() or c in ",/?!" for c in user_input) and "cya" not in user_input.lower()
    
        # Check if the user input is a single word and request more context if so
        if not is_amharic:
            filtered_response = "እባክዎን ጥያቄዎን በአማርኛ ቋንቋ ብቻ ያቅርቡ"
            return user_input, predicted_intent, filtered_response
        # elif len(user_input.split()) <= 1 and user_input not in single_words:
        elif len([word for word in user_input if word != " " and word != "" ]) <= 1 and user_input not in single_words:
            filtered_response = np.random.choice(["የእርስዎ ግብዓት በጣም አጭር ነው። እባክዎ ተጨማሪ አውድ ወይም የተሟላ ዓረፍተ ነገር ያቅርቡ።",
                                                  "ይቅርታ፣ አልገባኝም እባክህ እንደገና መግለጽ ትችላለህ ወይስ ሌላ ጥያቄ ጠይቅ?",
                                                  "ይቅርታ፣ ተጨማሪ ዝርዝሮችን መስጠት ትችላለህ ወይም ሌላ ጥያቄ መሞከር ትችላለህ?"])
            return user_input, predicted_intent, filtered_response
        else:
            # Convert the user input into a numerical representation
            user_input_features = vectorizer.transform([user_input])
            # Handle the case where the user input is not found in the dataset
            if user_input_features.nnz == 0:
                filtered_response = "ተጨማሪ ዝርዝሮችን መስጠት ትችላለህ ወይም ሌላ ጥያቄ መሞከር ትችላለህ?"
                return user_input, predicted_intent, filtered_response

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

@app.route('/process_input', methods=['POST'])
def process_input():
    try:
        data = request.get_json()
        user_input = data['user_input']
        user_input = remove_prefix(user_input)
        print (user_input)
        _, predicted_intent, filtered_response = process_user_input(user_input, intent_classifier, vectorizer, intent_responses)
        return jsonify({'predicted_intent': predicted_intent, 'filtered_response': filtered_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def hello():
    try:
        return "helooooo"
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load intents from a JSON file
    with open('data/amharic_intent.json', 'r', encoding='utf-8') as file:
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
    # vectorizer = CountVectorizer(lowercase=True, token_pattern=r'\b\w+\b', ngram_range=(1, 2))
    vectorizer = TfidfVectorizer(lowercase=True, token_pattern=r'\b\w+\b', ngram_range=(1, 2))
    train_features = vectorizer.fit_transform(train_texts)

    # Train a logistic regression model for intent recognition
    intent_classifier = SVC(kernel='linear')
    # intent_classifier = LogisticRegression()
    intent_classifier.fit(train_features, train_labels)

  
    app.run(debug=True, host='0.0.0.0')
