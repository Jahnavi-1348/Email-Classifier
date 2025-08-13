import joblib
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    model = joblib.load("saved_models/mail_classifier_model.pkl")
    vectorizer = joblib.load("saved_models/tfidf_vectorizer.pkl")
    logging.info("Model and vectorizer loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model or vectorizer: {e}")
    sys.exit(1)

def classify_texts(texts):
    try:
        X_vec = vectorizer.transform(texts)
        preds = model.predict(X_vec)
        return preds
    except Exception as e:
        logging.error(f"Error during classification: {e}")
        raise
