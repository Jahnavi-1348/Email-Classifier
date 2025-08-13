# train_model.py
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load data
dataset_path = r"C:\Users\jahna\Downloads\ed\Rejection Data - Sheet1.csv"
data = pd.read_csv(dataset_path)

# Create binary reject column
condition = data['Status'] == 'not_reject'
reversed_binary = (1 - condition.astype(int))
data['reject'] = reversed_binary

# Split data
x = data['Email']
y = data['reject']
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# Vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
x_train_vec = vectorizer.fit_transform(x_train.astype(str))
x_test_vec = vectorizer.transform(x_test.astype(str))

# Model
model = LogisticRegression()
model.fit(x_train_vec, y_train)

# Evaluation
y_pred = model.predict(x_test_vec)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model and vectorizer
##@@##

# Ensure folder exists
import os
os.makedirs('saved_models', exist_ok=True)

# Save model and vectorizer
joblib.dump(model, 'saved_models/mail_classifier_model.pkl')
joblib.dump(vectorizer, 'saved_models/tfidf_vectorizer.pkl')


