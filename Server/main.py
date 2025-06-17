from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

# Load model and vectorizer
with open("model/fake_news_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

app = Flask(__name__)
CORS(app)  # Allow CORS

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    news_text = data.get("text", "")

    if not news_text.strip():
        return jsonify({"result": "No text provided"}), 400

    # Vectorize the input text
    vectorized_text = vectorizer.transform([news_text])
    
    # Predict using the model
    prediction = model.predict(vectorized_text)[0]
    result = "Real" if prediction == 1 else "Fake"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
