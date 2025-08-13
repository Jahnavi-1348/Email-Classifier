# Email-Classifier
A FastAPI-based machine learning API for classifying emails into predefined categories.This project uses Docker for deployment.

Features
*REST API built with FastAPI
*Machine Learning-powered email classification
*Dockerized for easy deployment
*JSON-based request/response format

Install Dependencies
pip install -r requirements.txt

Run Locally
uvicorn app.main:app --reload

Build Image
docker build -t email-classifier .

Run Container
docker run -p 8000:8000 email-classifier

Access the API
Swagger UI: http://localhost:8000/docs

Root endpoint: http://localhost:8000
