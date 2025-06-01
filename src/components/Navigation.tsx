'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
  const pathname = usePathname();
  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-blue-900/80 backdrop-blur-lg fixed w-full z-50 shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-2xl font-extrabold text-white tracking-wide drop-shadow-lg">
            IPL Predictor
          </Link>
          <div className="flex space-x-8">
            <Link
              href="/"
              className={`text-base font-medium transition-colors ${isActive('/') ? 'text-green-400' : 'text-gray-200 hover:text-white'}`}
            >
              Home
            </Link>
            <Link
              href="/predict"
              className={`text-base font-medium transition-colors ${isActive('/predict') ? 'text-green-400' : 'text-gray-200 hover:text-white'}`}
            >
              Predict
            </Link>
            <Link
              href="/stats"
              className={`text-base font-medium transition-colors ${isActive('/stats') ? 'text-green-400' : 'text-gray-200 hover:text-white'}`}
            >
              Stats
            </Link>
            <Link
              href="/about"
              className={`text-base font-medium transition-colors ${isActive('/about') ? 'text-green-400' : 'text-gray-200 hover:text-white'}`}
            >
              About
            </Link>
            <Link
              href="/contact"
              className={`text-base font-medium transition-colors ${isActive('/contact') ? 'text-green-400' : 'text-gray-200 hover:text-white'}`}
            >
              Contact
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
} 