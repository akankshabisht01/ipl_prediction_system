import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { GiCricketBat } from 'react-icons/gi';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-black text-white flex items-center justify-center">
      <div className="w-full max-w-7xl px-8 py-20 flex flex-col md:flex-row items-center gap-12 md:gap-20">
        {/* Left: Text Content */}
        <div className="flex-1 flex flex-col justify-center items-start space-y-8">
          <div className="flex items-center space-x-3 mb-2">
            <GiCricketBat className="text-4xl text-green-400 drop-shadow-lg animate-bounce" />
            <h1 className="text-5xl md:text-6xl font-extrabold leading-tight tracking-tight drop-shadow-lg">
              IPL Match Prediction
            </h1>
          </div>
          <p className="text-xl md:text-2xl text-gray-200 font-light max-w-2xl">
            Welcome to the IPL Match Prediction platform! Dive into the world of cricket analytics and get insights on upcoming matches. Explore team stats, trends, and make your own predictions for the Indian Premier League!
          </p>
          <div>
            <h2 className="text-2xl font-semibold text-blue-300 mb-2">Key Features:</h2>
            <ul className="space-y-2 text-base md:text-lg">
              <li className="flex items-center space-x-2">
                <span className="text-green-400">•</span>
                <span>ML-based match predictions</span>
              </li>
              <li className="flex items-center space-x-2">
                <span className="text-green-400">•</span>
                <span>Historical & live data analysis</span>
              </li>
              <li className="flex items-center space-x-2">
                <span className="text-green-400">•</span>
                <span>Team dashboards & stats</span>
              </li>
              <li className="flex items-center space-x-2">
                <span className="text-green-400">•</span>
                <span>Modern, interactive UI</span>
              </li>
            </ul>
          </div>
          <Link
            href="/predict"
            className="inline-block bg-gradient-to-r from-green-400 to-blue-500 hover:from-blue-500 hover:to-green-400 text-white text-2xl font-bold py-4 px-10 rounded-xl shadow-xl transform hover:scale-105 transition-all duration-300 animate-pulse"
          >
            Start Predicting Now
          </Link>
        </div>
        {/* Right: Image */}
        <div className="flex-1 flex items-center justify-center w-full h-[350px]">
          <div className="relative w-full h-full max-w-lg aspect-[16/9] rounded-2xl overflow-hidden shadow-2xl border-4 border-blue-800/40 bg-white/20 flex items-center justify-center">
            <Image
              src="/images/OIP.jpg"
              alt="Cricket Hero"
              fill
              className="object-contain object-center"
              priority
            />
          </div>
        </div>
      </div>
    </div>
  );
}
