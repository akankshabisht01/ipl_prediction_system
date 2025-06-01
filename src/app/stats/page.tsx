import Image from 'next/image';
import { GiCricketBat } from 'react-icons/gi';

const teams = [
  { name: 'Mumbai Indians', shortName: 'MI', color: 'from-blue-500 to-blue-700', stats: { matches: 247, wins: 138, losses: 105, trophies: 5 } },
  { name: 'Chennai Super Kings', shortName: 'CSK', color: 'from-yellow-400 to-yellow-600', stats: { matches: 225, wins: 131, losses: 91, trophies: 5 } },
  { name: 'Kolkata Knight Riders', shortName: 'KKR', color: 'from-purple-500 to-purple-700', stats: { matches: 237, wins: 119, losses: 114, trophies: 2 } },
  { name: 'Royal Challengers Bangalore', shortName: 'RCB', color: 'from-red-500 to-red-700', stats: { matches: 241, wins: 114, losses: 120, trophies: 0 } },
  { name: 'Delhi Capitals', shortName: 'DC', color: 'from-blue-600 to-blue-800', stats: { matches: 238, wins: 105, losses: 127, trophies: 0 } },
  { name: 'Rajasthan Royals', shortName: 'RR', color: 'from-pink-400 to-pink-600', stats: { matches: 206, wins: 101, losses: 100, trophies: 1 } },
  { name: 'Sunrisers Hyderabad', shortName: 'SRH', color: 'from-orange-400 to-orange-600', stats: { matches: 166, wins: 78, losses: 84, trophies: 1 } },
  { name: 'Punjab Kings', shortName: 'PBKS', color: 'from-red-600 to-red-800', stats: { matches: 232, wins: 104, losses: 124, trophies: 0 } },
];

export default function Stats() {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-black text-white py-16 px-4">
      <div className="absolute inset-0 -z-10 opacity-20">
        <Image src="/images/OIP.jpg" alt="Cricket" fill className="object-cover object-center" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-blue-900/60 to-transparent" />
      </div>
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-center mb-8">
          <GiCricketBat className="text-4xl text-green-400 drop-shadow-lg mr-3 animate-bounce" />
          <h1 className="text-4xl font-extrabold text-blue-300 drop-shadow-lg">IPL Team Statistics</h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {teams.map((team) => (
            <div key={team.shortName} className={`bg-gradient-to-br ${team.color} rounded-3xl p-8 shadow-xl border border-blue-800/40 backdrop-blur-lg bg-white/10 hover:scale-105 transition-transform duration-300`}>
              <h2 className="text-2xl font-bold mb-4 text-white flex items-center gap-2">
                <GiCricketBat className="text-green-300" /> {team.name}
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/20 rounded p-3 text-center">
                  <p className="text-sm opacity-80">Matches</p>
                  <p className="text-2xl font-bold">{team.stats.matches}</p>
                </div>
                <div className="bg-white/20 rounded p-3 text-center">
                  <p className="text-sm opacity-80">Wins</p>
                  <p className="text-2xl font-bold text-green-300">{team.stats.wins}</p>
                </div>
                <div className="bg-white/20 rounded p-3 text-center">
                  <p className="text-sm opacity-80">Losses</p>
                  <p className="text-2xl font-bold text-red-300">{team.stats.losses}</p>
                </div>
                <div className="bg-white/20 rounded p-3 text-center">
                  <p className="text-sm opacity-80">Trophies</p>
                  <p className="text-2xl font-bold text-yellow-300">{team.stats.trophies}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 