import React, { useState } from 'react';
import axios from 'axios';
import { API_BASE } from '../config';

function BlankPage5() {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setPrediction(null);
    setError('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select an image first.');
      return;
    }

    setLoading(true);
    setError('');
    setPrediction(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const res = await axios.post(`${API_BASE}/predict_ultrasound`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setPrediction(res.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.error ||
          'Failed to get prediction. Make sure the backend (app.py) is running.'
      );
    }

    setLoading(false);
  };

  return (
    <div className="page-wrapper">
      <h2 style={{ textAlign: 'center', marginTop: '50px' }}>
        Fetal Head Ultrasound Classification
      </h2>

      <div style={{ textAlign: 'center', marginTop: '30px' }}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <br />
        <button onClick={handleUpload} style={{ marginTop: '20px' }}>
          Upload & Predict
        </button>
      </div>

      {loading && <p style={{ textAlign: 'center' }}>Analyzing image...</p>}
      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
      {prediction && (
        <div style={{ textAlign: 'center', marginTop: '30px' }}>
          <h3>Prediction Result:</h3>
          <p><strong>Class:</strong> {prediction.predicted_class}</p>
          <p><strong>Confidence:</strong> {Number(prediction.confidence).toFixed(2)}%</p>
        </div>
      )}

      <footer className="site-footer">
        <p>&copy; {new Date().getFullYear()} Preterm and Women Health. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default BlankPage5;
