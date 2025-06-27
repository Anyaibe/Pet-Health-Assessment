from flask import Flask, render_template, request
<<<<<<< HEAD
import sqlite3
import pickle
import pandas as pd

# Load the original dataset with emergency flags
df = pd.read_csv("pet_allergy_dataset.csv")

# Create a dictionary: condition -> emergency flag
emergency_dict = df.drop_duplicates("possible_condition").set_index("possible_condition")["emergency"].to_dict()

app = Flask(__name__)

# Load ML model
with open("pet_health_model.pkl", "rb") as f:
    model, symptom_list, le_condition = pickle.load(f)

@app.route("/")
def index():
    return render_template("index.html", symptoms=symptom_list)

# ✅ RIGHT HERE: This is the correct place to define the assess route
@app.route("/assess", methods=["POST"])
def assess():
    # Get user input
    pet_type = request.form["pet_type"]
    age = int(request.form.get("age", 0))
    selected = request.form.getlist("symptoms")

    # Create binary feature vector (age + symptoms)
    features = [age] + [1 if s in selected else 0 for s in symptom_list]
    
    # Predict condition
    prediction = model.predict([features])[0]
    predicted_condition = le_condition.inverse_transform([prediction])[0]

    # ✅ Emergency condition check
    EMERGENCY_CONDITIONS = {
        "respiratory distress",
        "feline leukemia",
        "canine parvovirus"
    }
    emergency_flag = int(emergency_dict.get(predicted_condition, 0))


    # Severity scoring logic
    severity_score = 2 * len(selected)

    # Save result to database
    conn = sqlite3.connect("pet_health.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO assessments (pet_type, age, symptoms, conditions, severity_score, emergency_flag)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        pet_type,
        age,
        ", ".join(selected),
        predicted_condition,
        severity_score,
        emergency_flag
    ))
    conn.commit()
    conn.close()

    return render_template("result.html",
        results=[(", ".join(selected), predicted_condition)],
        score=severity_score,
        emergency=emergency_flag
    )


# ✅ Route: View history
@app.route("/history")
def history():
    conn = sqlite3.connect("pet_health.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assessments ORDER BY timestamp DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template("history.html", records=records)

# ✅ Run the app
=======

app = Flask(__name__)

# Sample condition database (extendable)
conditions_db = {
    "dog": {
        "lethargy": ("Canine Parvovirus", "high"),
        "vomiting": ("Gastroenteritis", "medium"),
        "difficulty breathing": ("Respiratory Distress", "emergency"),
        "itchy skin": ("Allergic Dermatitis", "low")
    },
    "cat": {
        "lethargy": ("Feline Leukemia", "high"),
        "vomiting": ("Hairball blockage", "medium"),
        "difficulty breathing": ("Asthma", "emergency"),
        "itchy skin": ("Fleas or Allergies", "low")
    }
}

@app.route("/", methods=["GET", "POST"])
def index():
    symptoms = list({symptom for pet in conditions_db for symptom in conditions_db[pet]})
    return render_template("index.html", symptoms=symptoms)

@app.route("/assess", methods=["POST"])
def assess():
    pet_type = request.form["pet_type"]
    selected_symptoms = request.form.getlist("symptoms")

    results = []
    severity_score = 0
    emergency_flag = False

    for symptom in selected_symptoms:
        if symptom in conditions_db[pet_type]:
            condition, severity = conditions_db[pet_type][symptom]
            results.append((symptom, condition, severity))
            if severity == "emergency":
                emergency_flag = True
                severity_score += 5
            elif severity == "high":
                severity_score += 3
            elif severity == "medium":
                severity_score += 2
            else:
                severity_score += 1

    return render_template("result.html", results=results, score=severity_score, emergency=emergency_flag)

>>>>>>> af79d483e0e83e3265f201d2e751ac3a6573c855
if __name__ == "__main__":
    app.run(debug=True)
