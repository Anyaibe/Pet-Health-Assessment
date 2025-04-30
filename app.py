from flask import Flask, render_template, request

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

if __name__ == "__main__":
    app.run(debug=True)
