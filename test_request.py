import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "model": "svm",  # You can change this to "knn" to test that model too
    "features": {
        "age_group": "30-34",
        "reported_race_ethnicity": "Black",
        "tobacco_use_during_pregnancy": "No",
        "adequate_prenatal_care": "Adequate",
        "previous_births": "Two"
    }
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
