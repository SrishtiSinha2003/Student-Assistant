# Student Assistant

A smart Flask-based web application designed to assist students in career planning, resume evaluation, and study plan generation using machine learning models.

## 🚀 Features

- **Career Guidance**: Predicts suitable career options based on input.
- **Resume Scoring**: Evaluates resumes and provides feedback.
- **Study Plan Generator**: Creates a personalized study schedule.
- **Interactive Web Interface**: Built with Flask and templates.
- **Deployment Ready**: Includes `render.yaml` and `gunicorn` for deployment on platforms like Render.

## 🧠 Technologies Used

- **Flask** for web framework
- **Python** for backend logic
- **Pickle (.pkl)** for ML models
- **Scikit-learn, Pandas, NumPy** for model training (via `.ipynb` notebooks)
- **Gunicorn** for WSGI HTTP server
- **HTML/CSS** for templates

## 📁 Project Structure
├── app/               # Flask app folder
│   └── templates/     # HTML templates
├── app.py             # Main Flask application script
├── run.py             # Alternate app runner
├── render.yaml        # Deployment configuration
├── requirements.txt   # Python dependencies
├── *.pkl              # Trained ML model files
├── *.ipynb            # Jupyter notebooks for model training
├── *.csv              # Sample dataset files
├── *.py               # Supporting Python scripts
└── README.md          # This file

