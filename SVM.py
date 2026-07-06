# svm.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score
import joblib
import os

# Debug: show where the script is running from
print("📁 Running from:", os.getcwd())

# Load dataset
file_path = os.path.join(os.getcwd(), "births.csv")
print("📄 Loading CSV from:", file_path)
df = pd.read_csv(file_path, low_memory=False)

# Shuffle and reduce data
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df = df.iloc[:107151]

# Encode categorical variables
categorical_columns = ["age_group", "reported_race_ethnicity", "tobacco_use_during_pregnancy", "adequate_prenatal_care"]
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Process previous_births
df["previous_births"] = df["previous_births"].replace({
    "None": 0,
    "One": 1,
    "Two": 2,
    "Three or More": 3,
    "One, Two, Three or More": 3
})
df["previous_births"] = df["previous_births"].fillna(0).astype(int)

# Train/test split
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
X_train = train_df.drop(columns=["preterm_indicator"])
y_train = train_df["preterm_indicator"]
X_val = val_df.drop(columns=["preterm_indicator"])
y_val = val_df["preterm_indicator"]

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Train the SVM model
print("⚙️ Training SVM model...")
svm_model = SVC(kernel="linear", random_state=42, class_weight='balanced', probability=True)
svm_model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = svm_model.predict(X_val_scaled)
acc = accuracy_score(y_val, y_pred)
f1 = f1_score(y_val, y_pred)
print(f"✅ SVM Accuracy: {acc:.4f}")
print(f"✅ SVM F1 Score: {f1:.4f}")

# Save model and components
try:
    joblib.dump(svm_model, "svm_model.joblib")
    print("[OK] Saved svm_model.joblib")

    joblib.dump(label_encoders, "svm_encoders.joblib")
    print("[OK] Saved svm_encoders.joblib")

    joblib.dump(scaler, "svm_scaler.joblib")
    print("[OK] Saved svm_scaler.joblib")

    print("✅ SVM model, encoders, and scaler saved successfully.")

except Exception as e:
    print("❌ Failed to save one or more SVM files:", str(e))
