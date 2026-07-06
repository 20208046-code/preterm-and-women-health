# knn.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib
import os

# Use relative path
file_path = os.path.join(os.getcwd(), "births.csv")

df = pd.read_csv(file_path, low_memory=False)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df = df.iloc[:107151]

categorical_columns = ["age_group", "reported_race_ethnicity", "tobacco_use_during_pregnancy", "adequate_prenatal_care"]

label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

df["previous_births"] = df["previous_births"].replace({
    "None": 0,
    "One": 1,
    "Two": 2,
    "Three or More": 3,
    "One, Two, Three or More": 3
})
df["previous_births"] = df["previous_births"].fillna(0).astype(int)

train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

X_train = train_df.drop(columns=["preterm_indicator"])
y_train = train_df["preterm_indicator"]
X_val = val_df.drop(columns=["preterm_indicator"])
y_val = val_df["preterm_indicator"]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

k = 3
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train_scaled, y_train)

y_pred_knn = knn.predict(X_val_scaled)

accuracy_knn = accuracy_score(y_val, y_pred_knn)
f1_knn = f1_score(y_val, y_pred_knn)

# Save model, encoders, and scaler
joblib.dump(knn, "knn_model.joblib")
joblib.dump(label_encoders, "knn_encoders.joblib")
joblib.dump(scaler, "knn_scaler.joblib")

print(f"KNN Accuracy: {accuracy_knn:.4f}")
print(f"KNN F1 Score: {f1_knn:.4f}")
print("KNN model, encoders, and scaler saved successfully.")
