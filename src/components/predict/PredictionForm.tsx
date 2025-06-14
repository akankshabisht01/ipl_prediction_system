'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';

const teams = [
  'Royal Challengers Bangalore',
  'Punjab Kings',
  'Delhi Capitals',
  'Mumbai Indians',
  'Kolkata Knight Riders',
  'Rajasthan Royals',
  'Sunrisers Hyderabad',
  'Chennai Super Kings',
  'Kochi Tuskers Kerala',
  'Gujarat Titans',
  'Lucknow Super Giants',
  'Royal Challengers Bengaluru',
];

const venues = [
  'Wankhede Stadium, Mumbai',
  'M. A. Chidambaram Stadium, Chennai',
  'Eden Gardens, Kolkata',
  'Arun Jaitley Stadium, Delhi',
  'M. Chinnaswamy Stadium, Bengaluru',
  'Punjab Cricket Association IS Bindra Stadium, Mohali',
  'Sawai Mansingh Stadium, Jaipur',
  'Rajiv Gandhi International Cricket Stadium, Hyderabad',
  'Sardar Patel Stadium (Narendra Modi Stadium), Ahmedabad',
  'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow',
  'Dr. DY Patil Sports Academy, Mumbai',
  'Barabati Stadium, Cuttack',
  'Holkar Cricket Stadium, Indore',
  'JSCA International Stadium Complex, Ranchi',
  'Green Park Stadium, Kanpur',
  'Zayed Cricket Stadium, Abu Dhabi',
];

interface PredictionFormProps {
  onSubmit: (formData: any) => void;
}

export default function PredictionForm({ onSubmit }: PredictionFormProps) {
  const [formData, setFormData] = useState({
    batting_team: '',
    bowling_team: '',
    venue: '',
    runs_left: '',
    balls_left: '',
    wickets_left: '',
    total_runs_x: '',
    crr: '',
    rrr: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Convert numeric fields
    onSubmit({
      ...formData,
      runs_left: Number(formData.runs_left),
      balls_left: Number(formData.balls_left),
      wickets_left: Number(formData.wickets_left),
      total_runs_x: Number(formData.total_runs_x),
      crr: Number(formData.crr),
      rrr: Number(formData.rrr),
    });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="max-w-2xl mx-auto p-8 bg-[#232f47] rounded-2xl shadow-2xl border border-[#26334d] text-white"
    >
      <form onSubmit={handleSubmit} className="space-y-8">
        <div className="space-y-6">
          <div>
            <label htmlFor="batting_team" className="block text-sm font-medium leading-6 text-white">Batting Team</label>
            <select
              id="batting_team"
              name="batting_team"
              value={formData.batting_team}
              onChange={handleChange}
              required
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            >
              <option value="">Select Batting Team</option>
              {teams.map((team) => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="bowling_team" className="block text-sm font-medium leading-6 text-white">Bowling Team</label>
            <select
              id="bowling_team"
              name="bowling_team"
              value={formData.bowling_team}
              onChange={handleChange}
              required
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            >
              <option value="">Select Bowling Team</option>
              {teams.filter((team) => team !== formData.batting_team).map((team) => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="venue" className="block text-sm font-medium leading-6 text-white">Venue</label>
            <select
              id="venue"
              name="venue"
              value={formData.venue}
              onChange={handleChange}
              required
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            >
              <option value="">Select Venue</option>
              {venues.map((venue) => (
                <option key={venue} value={venue}>{venue}</option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="runs_left" className="block text-sm font-medium leading-6 text-white">Runs Left</label>
            <input
              type="number"
              id="runs_left"
              name="runs_left"
              value={formData.runs_left}
              onChange={handleChange}
              required
              min="0"
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            />
          </div>
          <div>
            <label htmlFor="balls_left" className="block text-sm font-medium leading-6 text-white">Balls Left</label>
            <input
              type="number"
              id="balls_left"
              name="balls_left"
              value={formData.balls_left}
              onChange={handleChange}
              required
              min="0"
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            />
          </div>
          <div>
            <label htmlFor="wickets_left" className="block text-sm font-medium leading-6 text-white">Wickets Left</label>
            <input
              type="number"
              id="wickets_left"
              name="wickets_left"
              value={formData.wickets_left}
              onChange={handleChange}
              required
              min="0"
              max="10"
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            />
          </div>
          <div>
            <label htmlFor="total_runs_x" className="block text-sm font-medium leading-6 text-white">Target Runs</label>
            <input
              type="number"
              id="total_runs_x"
              name="total_runs_x"
              value={formData.total_runs_x}
              onChange={handleChange}
              required
              min="0"
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            />
          </div>
          <div>
            <label htmlFor="crr" className="block text-sm font-medium leading-6 text-white">Current Run Rate (CRR)</label>
            <input
              type="number"
              step="0.01"
              id="crr"
              name="crr"
              value={formData.crr}
              onChange={handleChange}
              required
              min="0"
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            />
          </div>
          <div>
            <label htmlFor="rrr" className="block text-sm font-medium leading-6 text-white">Required Run Rate (RRR)</label>
            <input
              type="number"
              step="0.01"
              id="rrr"
              name="rrr"
              value={formData.rrr}
              onChange={handleChange}
              required
              min="0"
              className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-white bg-[#1a2336] ring-1 ring-inset ring-[#26334d] focus:ring-2 focus:ring-ipl-blue focus:bg-[#232f47] sm:text-sm sm:leading-6"
            />
          </div>
        </div>
        <div>
          <button
            type="submit"
            className="w-full rounded-lg bg-ipl-blue px-8 py-4 text-lg font-bold text-white shadow-lg hover:bg-ipl-blue/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ipl-blue transition-all duration-200"
          >
            Predict Winner
          </button>
        </div>
      </form>
    </motion.div>
  );
}
