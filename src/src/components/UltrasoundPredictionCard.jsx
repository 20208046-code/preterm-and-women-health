import React, { useState } from 'react';

function UltrasoundPredictionCard() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFile(e.target.files[0]);
    setResult('');
  };

  const handleUpload = async () => {
    if (!file) {
      setResult('Please select an image.');
      return;
    }

    const formData = new FormData();
    formData.append('image', file);

    setLoading(true);
    setResult('');

    try {
      const response = await fetch('http://localhost:5000/predict_ultrasound', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        setResult(`Error: ${data.error}`);
      } else {
        setResult(
          `Prediction: ${data.predicted_class} (Confidence: ${data.confidence}%)`
        );
      }
    } catch (error) {
      setResult('Error: Could not connect to the prediction server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-4 shadow-md rounded-xl bg-white">
      <h2 className="text-xl font-semibold mb-2">Ultrasound Image Prediction</h2>
      <input type="file" accept="image/*" onChange={handleChange} className="mb-2" />
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Predict
      </button>
      {loading && <p className="mt-2">Predicting...</p>}
      {result && <p className="mt-2 font-medium text-green-700">{result}</p>}
    </div>
  );
}

export default UltrasoundPredictionCard;
