from datetime import datetime, timedelta

def generate_study_plan(subjects, total_hours, deadline, study_method):
    plan = {}
    today = datetime.today().date()
    end_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    days_available = (end_date - today).days + 1

    if days_available <= 0:
        return {"error": "Deadline must be in the future."}

    hours_per_day = total_hours / days_available
    hours_per_subject_per_day = hours_per_day / len(subjects)

    current_date = today
    while current_date <= end_date:
        plan[str(current_date)] = {}
        for subject in subjects:
            plan[str(current_date)][subject] = {
                "hours": round(hours_per_subject_per_day, 2),
                "method": study_method
            }
        current_date += timedelta(days=1)

    return plan
