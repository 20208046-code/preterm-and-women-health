// src/pages/BlankPage4.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { API_BASE } from '../config';

// Option values MUST exactly match the label encoders the models were trained on.
const AGE_GROUPS = [
  'Under 15 yrs', '15 to 17 yrs', '18 to 19 yrs', '20 to 24 yrs',
  '25 to 29 yrs', '30 to 34 yrs', '35 to 39 yrs', '40 to 44 yrs',
  '45 to 49 yrs', '50+ yrs',
];
const RACES = [
  'White, non-Hispanic', 'Black, non-Hispanic',
  'Hispanic (of any race)', 'Asian, non-Hispanic',
];
const BIRTHS = ['None', 'One', 'Two', 'Three or More'];

function BlankPage4() {
  const [formData, setFormData] = useState({
    model: 'svm',
    age_group: '20 to 24 yrs',
    reported_race_ethnicity: 'White, non-Hispanic',
    tobacco_use_during_pregnancy: 'No',
    adequate_prenatal_care: 'Adequate',
    previous_births: 'None',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    const { model, ...features } = formData;

    try {
      const res = await axios.post(`${API_BASE}/predict`, { model, features });
      if (res.data.error) {
        setError(res.data.error);
      } else {
        setResult({ model: res.data.model, prediction: res.data.prediction });
      }
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.error ||
          'Could not reach the prediction server. Make sure the backend (app.py) is running on ' +
            API_BASE
      );
    } finally {
      setLoading(false);
    }
  };

  const labelStyle = { display: 'block', marginBottom: '6px', fontWeight: 600, color: '#1c598f' };
  const fieldStyle = {
    width: '100%', padding: '10px', borderRadius: '8px',
    border: '1px solid #cdd7e1', marginBottom: '20px', fontSize: '15px',
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        background: 'linear-gradient(135deg,#1c598f,#437aaa,#be8ea0,#982f56)',
      }}
    >
      <div
        style={{
          flex: 1,
          padding: '60px 20px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'flex-start',
        }}
      >
        <div
          style={{
            background: '#fff',
            padding: '40px 30px',
            borderRadius: '16px',
            boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
            maxWidth: '700px',
            width: '100%',
            color: '#000',
          }}
        >
          <h2 style={{ textAlign: 'center', marginBottom: '8px', color: '#1c598f' }}>
            Preterm Risk Assessment
          </h2>
          <p style={{ textAlign: 'center', marginTop: 0, marginBottom: '30px', color: '#5a6b7b' }}>
            Powered by trained SVM / KNN models on U.S. natality data.
          </p>

          <form onSubmit={handleSubmit}>
            <label style={labelStyle}>Prediction Model</label>
            <select name="model" value={formData.model} onChange={handleChange} style={fieldStyle}>
              <option value="svm">Support Vector Machine (SVM)</option>
              <option value="knn">K-Nearest Neighbors (KNN)</option>
            </select>

            <label style={labelStyle}>Age Group</label>
            <select name="age_group" value={formData.age_group} onChange={handleChange} style={fieldStyle}>
              {AGE_GROUPS.map((v) => <option key={v} value={v}>{v}</option>)}
            </select>

            <label style={labelStyle}>Race / Ethnicity</label>
            <select
              name="reported_race_ethnicity"
              value={formData.reported_race_ethnicity}
              onChange={handleChange}
              style={fieldStyle}
            >
              {RACES.map((v) => <option key={v} value={v}>{v}</option>)}
            </select>

            <label style={labelStyle}>Previous Births</label>
            <select name="previous_births" value={formData.previous_births} onChange={handleChange} style={fieldStyle}>
              {BIRTHS.map((v) => <option key={v} value={v}>{v}</option>)}
            </select>

            <label style={labelStyle}>Tobacco Use During Pregnancy</label>
            <select
              name="tobacco_use_during_pregnancy"
              value={formData.tobacco_use_during_pregnancy}
              onChange={handleChange}
              style={fieldStyle}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
            </select>

            <label style={labelStyle}>Prenatal Care</label>
            <select
              name="adequate_prenatal_care"
              value={formData.adequate_prenatal_care}
              onChange={handleChange}
              style={fieldStyle}
            >
              <option value="Adequate">Adequate</option>
              <option value="Inadequate">Inadequate</option>
            </select>

            <button
              type="submit"
              disabled={loading}
              style={{
                marginTop: '10px',
                width: '100%',
                padding: '12px 25px',
                backgroundColor: '#437aaa',
                color: '#fff',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {loading ? 'Predicting…' : 'Predict Preterm Risk'}
            </button>
          </form>

          {error && (
            <p style={{ color: '#b00020', textAlign: 'center', marginTop: '20px' }}>{error}</p>
          )}

          {result && (
            <div
              style={{
                textAlign: 'center',
                marginTop: '30px',
                padding: '20px',
                borderRadius: '12px',
                background: result.prediction === 1 ? '#fdecef' : '#eaf6ec',
                border: `1px solid ${result.prediction === 1 ? '#e0a0ad' : '#a8d4b0'}`,
              }}
            >
              <h3 style={{ marginTop: 0 }}>Prediction Result</h3>
              <p style={{ fontSize: '20px', fontWeight: 700, color: result.prediction === 1 ? '#982f56' : '#1c7c3a' }}>
                {result.prediction === 1
                  ? 'Higher risk of preterm birth'
                  : 'Lower risk of preterm birth'}
              </p>
              <p style={{ color: '#5a6b7b' }}>
                Model: {result.model.toUpperCase()} · class label {result.prediction}
              </p>
              <p style={{ fontSize: '13px', color: '#8a97a3', marginBottom: 0 }}>
                This is a statistical estimate, not a medical diagnosis. Always consult a healthcare provider.
              </p>
            </div>
          )}
        </div>
      </div>

      <footer
        className="site-footer"
        style={{ backgroundColor: '#39536e', color: '#ffffff', textAlign: 'center', padding: '20px 0' }}
      >
        <p>&copy; {new Date().getFullYear()} Preterm and Women Health. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default BlankPage4;
