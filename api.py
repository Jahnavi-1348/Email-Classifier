from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from reader import fetch_latest_emails
from classify import classify_texts
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(title="Job Email Classifier API")

class Credentials(BaseModel):
    email: str
    password: str

class TextInput(BaseModel):
    email_text: str

@app.post("/fetch-and-classify")
def fetch_and_classify(creds: Credentials):
    emails = fetch_latest_emails(creds.email, creds.password)
    texts = [email["text"] for email in emails]
    preds = classify_texts(texts)
    results = []
    for email_obj, prediction in zip(emails, preds):
        label = "Rejected" if prediction == 1 else "Accepted"
        results.append({
            "subject": email_obj.get("subject", "(No Subject)"),
            "label": label
        })
    return results


@app.post("/classify-text")
def classify_manual_text(input_data: TextInput):
    pred = classify_texts([input_data.email_text])[0]
    label = "Rejected" if pred == 1 else "Accepted"
    return {"text": input_data.email_text, "label": label}