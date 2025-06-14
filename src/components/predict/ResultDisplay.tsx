import React from 'react';
import { motion } from 'framer-motion';

interface ResultDisplayProps {
  battingTeam: string;
  bowlingTeam: string;
  battingWin: number;
  bowlingWin: number;
}

export default function ResultDisplay({ battingTeam, bowlingTeam, battingWin, bowlingWin }: ResultDisplayProps) {
  // Determine winner and confidence
  const winner = battingWin > bowlingWin ? battingTeam : bowlingTeam;
  const confidence = Math.max(battingWin, bowlingWin);
  const isBattingWinner = battingWin > bowlingWin;
  // For circular progress
  const circleSize = 120;
  const strokeWidth = 12;
  const radius = (circleSize - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = isBattingWinner ? battingWin : bowlingWin;
  const progressOffset = circumference - (progress / 100) * circumference;
  const accentColor = isBattingWinner ? '#1e40af' : '#f59e42';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="max-w-2xl mx-auto mt-8 p-8 bg-[#232f47] rounded-2xl shadow-2xl text-center border border-[#26334d]"
    >
      <h2 className="text-xl font-semibold mb-2 text-white tracking-wide">Prediction Result</h2>
      <div className="flex flex-col md:flex-row items-center justify-center gap-8 mt-4">
        {/* Circular Progress */}
        <div className="flex-shrink-0">
          <svg width={circleSize} height={circleSize}>
            <circle
              cx={circleSize / 2}
              cy={circleSize / 2}
              r={radius}
              fill="none"
              stroke="#26334d"
              strokeWidth={strokeWidth}
            />
            <circle
              cx={circleSize / 2}
              cy={circleSize / 2}
              r={radius}
              fill="none"
              stroke={accentColor}
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={progressOffset}
              strokeLinecap="round"
              style={{ transition: 'stroke-dashoffset 1s' }}
            />
          </svg>
        </div>
        {/* Winner and Confidence */}
        <div className="flex-1 flex flex-col items-center justify-center">
          <div className="text-lg text-gray-300 font-medium mb-1">Predicted Winner</div>
          <div className="text-3xl md:text-4xl font-extrabold text-white mb-2 drop-shadow-lg">{winner}</div>
          <div className="text-base text-gray-400 font-medium mt-2">Confidence Level</div>
          <div className="text-3xl font-bold text-white mb-2">{confidence.toFixed(2)}%</div>
        </div>
      </div>
      {/* Horizontal Bar */}
      <div className="flex items-center justify-between mt-8 text-gray-400 text-sm font-medium">
        <span>{battingTeam}</span>
        <span>{bowlingTeam}</span>
      </div>
      <div className="w-full h-3 bg-[#1a2336] rounded-full mt-2 mb-2 flex overflow-hidden">
        <div
          className="h-3 rounded-l-full"
          style={{ width: `${battingWin}%`, background: '#1e40af', transition: 'width 1s' }}
        />
        <div
          className="h-3 rounded-r-full"
          style={{ width: `${bowlingWin}%`, background: '#f59e42', transition: 'width 1s' }}
        />
      </div>
    </motion.div>
  );
} 