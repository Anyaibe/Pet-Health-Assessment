import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Step 1: Load dataset
df = pd.read_csv("pet_allergy_dataset.csv")

# Step 2: Get all unique symptoms for encoding
all_symptoms = sorted(df['symptom'].unique())

# Step 3: Create binary symptom flags
X_symptoms = df['symptom'].str.get_dummies().reindex(columns=all_symptoms, fill_value=0)

# Step 4: Add a constant dummy age (model will accept real age from user later)
X_symptoms.insert(0, "age", 5)

# Step 5: Encode output labels (possible_condition)
le_condition = LabelEncoder()
y = le_condition.fit_transform(df['possible_condition'])

# Step 6: Train the decision tree
model = DecisionTreeClassifier(max_depth=4)
model.fit(X_symptoms, y)

# Step 7: Save model, symptom list, and label encoder
with open("pet_health_model.pkl", "wb") as f:
    pickle.dump((model, all_symptoms, le_condition), f)

print("✅ Model trained and saved as pet_health_model.pkl")
