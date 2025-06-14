import React from 'react';
import { motion } from 'framer-motion';

interface ResultDisplayProps {
  battingTeam: string;
  bowlingTeam: string;
  battingWin: number;
  bowlingWin: number;
}

function DonutChart({ value, color, label }: { value: number; color: string; label: string }) {
  const size = 110;
  const strokeWidth = 14;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;
  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="mb-2">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#26334d"
          strokeWidth={strokeWidth}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1 }}
        />
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dominantBaseline="central"
          fontSize="1.6em"
          fill="white"
          fontWeight="bold"
        >
          {value.toFixed(2)}%
        </text>
      </svg>
      <span className="text-base font-semibold text-white mt-1 drop-shadow">{label}</span>
    </div>
  );
}

export default function ResultDisplay({ battingTeam, bowlingTeam, battingWin, bowlingWin }: ResultDisplayProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="max-w-2xl mx-auto mt-8 p-8 bg-[#232f47] rounded-2xl shadow-2xl text-center border border-[#26334d]"
    >
      <h2 className="text-xl font-semibold mb-8 text-white tracking-wide">Prediction Result</h2>
      <div className="flex flex-col md:flex-row items-center justify-center gap-12">
        <DonutChart value={battingWin} color="#1e40af" label={battingTeam} />
        <DonutChart value={bowlingWin} color="#f59e42" label={bowlingTeam} />
      </div>
    </motion.div>
  );
} 