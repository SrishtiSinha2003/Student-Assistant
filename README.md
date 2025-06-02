### 🧠 Smart Student Assistant
An intelligent assistant that helps students by providing:

## 🚀 Features

- 📚 Study Plan Generator: Creates a personalized study schedule.

- 📄 Resume Builder with Score Preview: Evaluates resumes and provides feedback.

- 🧭 Career Suggestion Tool: Predicts suitable career options based on input.

- ❓ Doubt Resolver: Uses Wikipedia to answer academic questions.

- 🌐 Interactive Web Interface: Built using Flask and styled with HTML/CSS.


## 🧠 Technologies Used

- **Flask** for web framework
- **Python** for backend logic
- **Pickle (.pkl)** for ML models
- **Scikit-learn, Pandas, NumPy** for model training (via `.ipynb` notebooks)
- **Gunicorn** for WSGI HTTP server
- **HTML/CSS** for templates

## 📁 Project Structure
```bash
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

