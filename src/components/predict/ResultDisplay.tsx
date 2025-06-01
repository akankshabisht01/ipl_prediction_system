import React from 'react';
import { motion } from 'framer-motion';

interface ResultDisplayProps {
  battingTeam: string;
  bowlingTeam: string;
  battingWin: number;
  bowlingWin: number;
}

export default function ResultDisplay({ battingTeam, bowlingTeam, battingWin, bowlingWin }: ResultDisplayProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="max-w-xl mx-auto mt-8 p-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg text-center"
    >
      <h2 className="text-2xl font-bold mb-4 text-ipl-blue dark:text-ipl-orange">Prediction Result</h2>
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <span className="font-semibold text-lg text-gray-900 dark:text-white">{battingTeam} Win Probability:</span>
          <span className="text-xl font-bold text-ipl-blue dark:text-ipl-orange">{battingWin}%</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="font-semibold text-lg text-gray-900 dark:text-white">{bowlingTeam} Win Probability:</span>
          <span className="text-xl font-bold text-ipl-blue dark:text-ipl-orange">{bowlingWin}%</span>
        </div>
      </div>
    </motion.div>
  );
} 