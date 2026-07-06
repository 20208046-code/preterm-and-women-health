# Preterm and Women Health

A women's-health web app with machine-learning preterm-birth risk prediction.

- **Frontend** — React (Create React App), in `src/`
- **Backend** — Flask ML API (`app.py`) serving trained **SVM** and **KNN** models
  for tabular preterm-risk prediction, plus an optional fetal-ultrasound CNN.

## Quick start

```bash
./start.sh
```

This launches the Flask API on **http://localhost:5000** and the React app on
**http://localhost:3000**. Open the frontend in your browser.

## Manual start

**Backend**
```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python app.py          # http://localhost:5000
```

**Frontend** (in a second terminal)
```bash
npm install
npm start                          # http://localhost:3000
```

## Features

| Page | Route | Status |
|------|-------|--------|
| Home | `/` | Working |
| Pregnancy Symptoms Checker | `/symptoms` | Working |
| Pregnancy Complications | `/complications` | Working |
| Ovulation Calculator | `/ovulation` | Working |
| **Preterm Risk Assessment** | `/preterm` | Live SVM/KNN prediction via the API |
| Fetal Head Ultrasound | `/ultrasound` | Needs TensorFlow + model file (see below) |

## API

- `GET /health` — reports which models are loaded.
- `POST /predict` — body:
  ```json
  {
    "model": "svm",
    "features": {
      "age_group": "30 to 34 yrs",
      "reported_race_ethnicity": "Black, non-Hispanic",
      "tobacco_use_during_pregnancy": "No",
      "adequate_prenatal_care": "Adequate",
      "previous_births": "Two"
    }
  }
  ```
  Returns `{ "model": "svm", "prediction": 0 | 1 }` (1 = higher preterm risk).
- `POST /predict_ultrasound` — multipart image upload. Returns 503 unless the
  ultrasound model is available.

The frontend reads the API URL from `REACT_APP_API_BASE` (defaults to
`http://localhost:5000`), see `src/config.js`.

## Enabling the ultrasound feature (optional)

The fetal-ultrasound classifier is **not** active by default because it requires
TensorFlow and a trained model file that isn't included in this repo:

1. `./.venv/bin/python -m pip install tensorflow`
2. Place `efficientnet_fetal_ultrasound_model.h5` in the project root.

The backend degrades gracefully — all other features work without it.
