'use client';

import React, { useState } from 'react';
import PredictionForm from '@/components/predict/PredictionForm';
import ResultDisplay from '@/components/predict/ResultDisplay';

export default function PredictPage() {
  const [result, setResult] = useState<null | {
    battingTeam: string;
    bowlingTeam: string;
    battingWin: number;
    bowlingWin: number;
  }>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (formData: any) => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const response = await fetch(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Prediction failed');
      }
      
      const data = await response.json();
      console.log('Response data:', data); // Debug log
      
      if (!data.batting_win || !data.bowling_win) {
        throw new Error('Invalid prediction response');
      }

      setResult({
        battingTeam: formData.batting_team,
        bowlingTeam: formData.bowling_team,
        battingWin: Math.round(Number(data.batting_win) * 100),
        bowlingWin: Math.round(Number(data.bowling_win) * 100),
      });
    } catch (err: any) {
      console.error('Prediction error:', err); // Debug log
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12">
      <h1 className="text-3xl font-bold text-center text-ipl-blue dark:text-ipl-orange mb-8">IPL Match Prediction</h1>
      <PredictionForm onSubmit={handleSubmit} />
      {loading && <div className="text-center mt-6 text-lg text-gray-700 dark:text-gray-200">Predicting...</div>}
      {error && <div className="text-center mt-6 text-lg text-red-600">{error}</div>}
      {result && (
        <ResultDisplay
          battingTeam={result.battingTeam}
          bowlingTeam={result.bowlingTeam}
          battingWin={result.battingWin}
          bowlingWin={result.bowlingWin}
        />
      )}
    </div>
  );
} 