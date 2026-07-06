import React from 'react';
import UltrasoundPredictionCard from '../components/UltrasoundPredictionCard';

const Ultrasound = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Ultrasound Prediction</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Other cards if needed */}
        <UltrasoundPredictionCard />
      </div>
    </div>
  );
};

export default Ultrasound;
