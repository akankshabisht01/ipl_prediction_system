'use client';

import Link from 'next/link';
import { FaLinkedin, FaGithub, FaGlobe } from 'react-icons/fa';
import Image from 'next/image';

export default function About() {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-black text-white py-16 px-4 flex items-center justify-center">
      <div className="absolute inset-0 -z-10 opacity-30">
        <Image src="/images/OIP.jpg" alt="Cricket" fill className="object-cover object-center" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-blue-900/60 to-transparent" />
      </div>
      <div className="max-w-2xl w-full mx-auto bg-white/10 backdrop-blur-lg rounded-3xl p-10 shadow-2xl border border-blue-800/40">
        <h1 className="text-4xl font-extrabold mb-6 text-center text-blue-300 drop-shadow-lg">About Me</h1>
        <h2 className="text-2xl font-semibold mb-4 text-green-300 text-center">Akanksha Bisht</h2>
        <p className="text-lg mb-8 text-center text-gray-200">
          I am a passionate Data Science student and developer, currently working on exciting projects that combine my love for cricket and data analytics. This IPL Prediction project is one of my endeavors to create meaningful applications using machine learning and modern web technologies.
        </p>
        <div className="space-y-4">
          <h3 className="text-xl font-semibold mb-4 text-blue-200">Connect with Me</h3>
          <div className="flex flex-col space-y-4">
            <Link
              href="https://www.linkedin.com/in/akanksha-bisht-00a1951b7"
              className="flex items-center space-x-3 hover:text-blue-400 transition-colors text-lg"
              target="_blank"
            >
              <FaLinkedin className="text-2xl text-blue-400" />
              <span>LinkedIn Profile</span>
            </Link>
            <Link
              href="https://github.com/akankshabisht01"
              className="flex items-center space-x-3 hover:text-blue-400 transition-colors text-lg"
              target="_blank"
            >
              <FaGithub className="text-2xl text-gray-300" />
              <span>GitHub Profile</span>
            </Link>
            <Link
              href="https://sites.google.com/view/akankshabishtportfolio/home"
              className="flex items-center space-x-3 hover:text-blue-400 transition-colors text-lg"
              target="_blank"
            >
              <FaGlobe className="text-2xl text-green-300" />
              <span>Portfolio Website</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
} 