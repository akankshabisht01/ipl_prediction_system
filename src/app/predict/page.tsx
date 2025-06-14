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
  const [rawResponse, setRawResponse] = useState('');

  const handleSubmit = async (formData: any) => {
    setLoading(true);
    setError('');
    setResult(null);
    setRawResponse('');
    try {
      // Debug log: print outgoing payload
      console.log('Sending to backend:', formData);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      
      const rawText = await response.text();
      setRawResponse(rawText); // Always show the raw response
      let data;
      try {
        data = JSON.parse(rawText);
      } catch (e) {
        console.error('Failed to parse response as JSON:', rawText);
        setError('Backend did not return valid JSON: ' + rawText);
        setResult(null);
        return;
      }
      console.log('Response data:', data); // Debug log
      console.log('Response keys:', Object.keys(data));
      
      const hasBatting = 'batting_team_win_probability' in data;
      const hasBowling = 'bowling_team_win_probability' in data;
      const battingVal = data.batting_team_win_probability;
      const bowlingVal = data.bowling_team_win_probability;
      const battingNum = typeof battingVal === 'number' && !isNaN(battingVal);
      const bowlingNum = typeof bowlingVal === 'number' && !isNaN(bowlingVal);

      if (!hasBatting || !hasBowling || !battingNum || !bowlingNum) {
        setError(
          'Invalid prediction response.\n' +
          'Expected keys: batting_team_win_probability (number), bowling_team_win_probability (number).\n' +
          'Actual keys: ' + Object.keys(data).join(', ') + '\n' +
          'Values: ' + JSON.stringify(data) + '\n' +
          'Raw response: ' + rawText
        );
        setResult(null);
        return;
      }

      setResult({
        battingTeam: formData.batting_team,
        bowlingTeam: formData.bowling_team,
        battingWin: Number(battingVal),
        bowlingWin: Number(bowlingVal),
      });
      setError(''); // Clear any previous error
    } catch (err: any) {
      console.error('Prediction error:', err); // Debug log
      setError(typeof err === 'string' ? err : (err.message || JSON.stringify(err) || 'Something went wrong'));
      setResult(null);
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
      {rawResponse && (
        <div className="text-center mt-2 text-xs text-gray-500 break-all">Raw backend response: {rawResponse}</div>
      )}
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