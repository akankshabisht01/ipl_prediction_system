'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  ChartBarIcon,
  CpuChipIcon,
  UserGroupIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';

const features = [
  {
    name: 'Advanced Analytics',
    description: 'Utilize sophisticated machine learning algorithms to analyze team performance, player statistics, and historical match data.',
    icon: ChartBarIcon,
  },
  {
    name: 'Real-time Predictions',
    description: 'Get instant predictions based on the latest team compositions, player form, and match conditions.',
    icon: CpuChipIcon,
  },
  {
    name: 'Team Performance',
    description: 'Access detailed insights into team performance metrics, including win ratios, head-to-head records, and venue statistics.',
    icon: UserGroupIcon,
  },
  {
    name: 'Historical Data',
    description: 'Leverage years of IPL match data to make informed predictions about upcoming matches.',
    icon: ClockIcon,
  },
];

export default function Features() {
  return (
    <div className="bg-white dark:bg-gray-900 py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-base font-semibold leading-7 text-ipl-blue dark:text-ipl-orange"
          >
            Predict Smarter
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="mt-2 text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl"
          >
            Everything you need to predict IPL matches
          </motion.p>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300"
          >
            Our prediction system combines advanced analytics with real-time data to provide
            accurate match predictions and insights.
          </motion.p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-4">
            {features.map((feature, index) => (
              <motion.div
                key={feature.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: index * 0.2 }}
                className="flex flex-col"
              >
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900 dark:text-white">
                  <feature.icon
                    className="h-5 w-5 flex-none text-ipl-blue dark:text-ipl-orange"
                    aria-hidden="true"
                  />
                  {feature.name}
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600 dark:text-gray-300">
                  <p className="flex-auto">{feature.description}</p>
                </dd>
              </motion.div>
            ))}
          </dl>
        </div>
      </div>
    </div>
  );
}
