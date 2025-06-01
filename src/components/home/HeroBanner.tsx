'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import Image from 'next/image';

export default function HeroBanner() {
  return (
    <div className="relative isolate overflow-hidden bg-gradient-to-b from-ipl-blue/20 to-white dark:from-ipl-blue/10 dark:to-gray-900">
      <div className="mx-auto max-w-7xl px-6 pb-24 pt-10 sm:pb-32 lg:flex lg:px-8 lg:py-40">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mx-auto max-w-2xl flex-shrink-0 lg:mx-0 lg:max-w-xl lg:pt-8"
        >
          <div className="mt-24 sm:mt-32 lg:mt-16">
            <Link
              href="/predict"
              className="inline-flex space-x-6 rounded-full bg-ipl-orange px-3 py-1 text-sm font-semibold leading-6 text-white ring-1 ring-inset ring-ipl-orange/20 hover:bg-ipl-orange/90"
            >
              <span>Predict Now</span>
              <span aria-hidden="true">&rarr;</span>
            </Link>
          </div>
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="mt-10 text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl"
          >
            Predict IPL Matches with AI
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300"
          >
            Experience the future of cricket predictions with our advanced machine learning model.
            Get accurate predictions for IPL matches based on historical data and real-time statistics.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="mt-10 flex items-center gap-x-6"
          >
            <Link
              href="/predict"
              className="rounded-md bg-ipl-blue px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-ipl-blue/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ipl-blue"
            >
              Get Started
            </Link>
            <Link
              href="/about"
              className="text-sm font-semibold leading-6 text-gray-900 dark:text-white"
            >
              Learn more <span aria-hidden="true">→</span>
            </Link>
          </motion.div>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-10 lg:mr-0 lg:mt-0 lg:max-w-none lg:flex-none xl:ml-32"
        >
          <div className="max-w-3xl flex-none sm:max-w-5xl lg:max-w-none">
            <Image
              src="/images/OIP.jpg"
              alt="Cricket match illustration"
              width={800}
              height={400}
              className="w-[76rem] rounded-md bg-white/5 shadow-2xl ring-1 ring-white/10 object-contain"
            />
          </div>
        </motion.div>
      </div>
    </div>
  );
}
