from flask import Blueprint, request, jsonify
import joblib
import os

career = Blueprint('career', __name__)

# Load model and mlb once when blueprint is loaded
model_path = os.path.join(os.path.dirname(__file__), '..', 'career_model.pkl')
mlb_path = os.path.join(os.path.dirname(__file__), '..', 'mlb.pkl')

model = joblib.load(model_path)
mlb = joblib.load(mlb_path)

@career.route('/predict', methods=['POST'])
def predict_career():
    data = request.get_json()

    # Example input: {"skills": ["python", "machine learning"]}
    skills = data.get('skills', [])
    if not skills:
        return jsonify({'error': 'No skills provided'}), 400

    # Transform input using mlb
    skills_transformed = mlb.transform([skills])

    # Predict career
    prediction = model.predict(skills_transformed)[0]

    return jsonify({'predicted_career': prediction})
