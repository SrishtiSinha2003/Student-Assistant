#This folder holds your entire Flask backend logic: routes, database models, utility functions.

from argparse import Action
from flask import Flask, request, render_template, jsonify
from study_plan_generator import generate_study_plan  # Import your logic
import requests
app = Flask(__name__)
import joblib
import numpy as np
import wikipedia

#for home page 
@app.route('/')
def home():
    return render_template('home.html')


# logic for career suggestion system 
def career_suggestion(skills):
    career_map = {
        'python': ('Data Analyst', 3, ['https://www.coursera.org/learn/python-data-analysis']),
        'machine learning': ('Machine Learning Engineer', 5, ['https://www.coursera.org/learn/machine-learning']),
        'data analysis': ('Data Analyst', 4, ['https://www.edx.org/course/data-analysis']),
        'javascript': ('Web Developer', 4, ['https://www.freecodecamp.org/learn']),
        'html': ('Web Developer', 3, ['https://www.freecodecamp.org/learn']),
        'css': ('Web Developer', 3, ['https://www.freecodecamp.org/learn']),
        'management': ('Project Manager', 3, ['https://www.pmi.org/certifications/project-management-pmp']),
        'communication': ('HR Specialist', 2, ['https://www.udemy.com/course/hr-management']),
        'cloud': ('Cloud Engineer', 4, ['https://aws.amazon.com/training/']),
        'sql': ('Database Administrator', 3, ['https://www.codecademy.com/learn/learn-sql']),
    }

    scores = {}
    resources = {}

    for skill in skills:
        skill_lower = skill.strip().lower()
        if skill_lower in career_map:
            role, weight, links = career_map[skill_lower]
            scores[role] = scores.get(role, 0) + weight
            resources.setdefault(role, set()).update(links)

    if not scores:
        return [{'role': 'General Student', 'resources': []}]

    sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = []
    for role, _ in sorted_roles[:3]:
        results.append({'role': role, 'resources': list(resources[role])})
    return results

@app.route('/career-form', methods=['GET', 'POST'])
def career_form():
    if request.method == 'POST':
        # Collect form inputs
        education = request.form.get('education')
        skills = request.form.get('skills')
        interests = request.form.get('interests')
        experience = request.form.get('experience')

        # Call your suggestion logic (assuming it returns role dicts)
        roles = career_suggestion(education, skills, interests, experience)
        return render_template('career_form.html', roles=roles)

    return render_template('career_form.html')


#for resume bulder and resume scorer.  Load resume scoring ML model
resume_scorer = joblib.load('resume_score_model.pkl')
skills_vectorizer = joblib.load('skills_vectorizer.pkl')
education_encoder = joblib.load('education_encoder.pkl')


@app.route('/', methods=['GET', 'POST'])
def user_inp():
    roles = None
    if request.method == 'POST':
        skills_raw = request.form.get('skills')
        skills = [s.strip() for s in skills_raw.split(',')] if skills_raw else []
        roles = career_suggestion(skills)
    return render_template('career_form.html', roles=roles)

#logic for resume builder 
@app.route('/resume-builder', methods=['GET', 'POST'])
def resume_builder():
    if request.method == 'POST':
        action = request.form.get('action')
        # Extract resume form data
        name = request.form.get('name')
        contact = request.form.get('contact')
        job_title = request.form.get('job_title')
        skills = request.form.get('skills')  # comma separated string
        experience = request.form.get('experience')
        education = request.form.get('education')
        action = request.form.get('action')  # Get which button was clicked

        if action == 'preview':
            # Just render preview without scoring
            return render_template('resume_preview.html',
                                   name=name, contact=contact, job_title=job_title,
                                   skills=skills, experience=experience, education=education,
                                   score=None)

        elif action == 'submit':
            # Preprocess inputs for ML model
            input_features = preprocess_resume_features(skills, experience, education)

            # Predict score using ML model
            score = resume_scorer.predict(input_features)[0]
            score = round(score, 2)

            # Render preview with score
            return render_template('resume_preview.html',
                                   name=name, contact=contact, job_title=job_title,
                                   skills=skills, experience=experience, education=education,
                                   score=score)

    return render_template('resume_form.html')


# Dummy preprocessing function, you should replace with your actual preprocessing
def preprocess_resume_features(skills_str, experience, education):
    # Vectorize skills
    skills_vec = skills_vectorizer.transform([skills_str]).toarray()  # shape: (1, ~25)

    # Convert experience to float
    try:
        exp_years = float(experience)
    except:
        exp_years = 0.0
    exp_vec = np.array([[exp_years]])  # shape: (1, 1)

    # Encode education (label encoder output shape: (1,))
    education_enc = education_encoder.transform([education])
    education_vec = np.array(education_enc).reshape(1, -1)  # shape: (1, 1)

    # Combine all into a single feature vector
    full_features = np.hstack((skills_vec, exp_vec, education_vec))  # shape: (1, 28)
    return full_features

# for study plan generator 
@app.route('/study-plan', methods=['GET', 'POST'])
def study_plan():
    plan = None
    if request.method == 'POST':
        purpose = request.form.get('purpose')
        subjects = [s.strip() for s in request.form.get('subjects', '').split(',')]
        hours = float(request.form.get('hours'))
        deadline = request.form.get('deadline')
        method = request.form.get('method')
        plan = generate_study_plan(subjects, hours, deadline, method)
    return render_template('study_plan_form.html', plan=plan)

def generate_study_plan(subjects, hours, deadline, method):
    from datetime import datetime
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
    days_left = (deadline_date - datetime.now()).days

    if days_left <= 0:
        return "Deadline has already passed or is today. Please choose a future date."

    total_subjects = len(subjects)
    hours_per_subject_per_day = hours / total_subjects

    plan = {}
    for subject in subjects:
        plan[subject] = f"Study {hours_per_subject_per_day:.2f} hrs/day using {method} method for next {days_left} days"
    print(plan)
    return plan


# doubt resolver logic

@app.route('/resolve-doubt', methods=['GET', 'POST'])
def resolve_doubt():
    doubt= None
    result = None  # Initialize the variable to avoid UnboundLocalError

    if request.method == 'POST':
        doubt = request.form.get('doubt')
        try:
            result = wikipedia.summary(doubt, sentences=3)
        except wikipedia.exceptions.DisambiguationError as e:
            result = f"Your query is too broad. Suggestions: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            result = "Sorry, no matching article was found on Wikipedia."
        except Exception as ex:
            result = f"An unexpected error occurred: {str(ex)}"
    print(doubt,result)
    return render_template('doubt_form.html', result=result)


if __name__ == '__main__':
     app.run(debug=True)

