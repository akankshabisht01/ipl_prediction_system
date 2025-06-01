'use client';

import { FaEnvelope, FaPhone, FaMapMarkerAlt } from 'react-icons/fa';
import Image from 'next/image';

export default function Contact() {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-black text-white py-16 px-4 flex items-center justify-center">
      <div className="absolute inset-0 -z-10 opacity-30">
        <Image src="/images/OIP.jpg" alt="Cricket" fill className="object-cover object-center" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-blue-900/60 to-transparent" />
      </div>
      <div className="max-w-4xl w-full mx-auto grid md:grid-cols-2 gap-8 bg-white/10 backdrop-blur-lg rounded-3xl p-10 shadow-2xl border border-blue-800/40">
        <div>
          <h1 className="text-4xl font-extrabold mb-6 text-blue-300 drop-shadow-lg">Contact Me</h1>
          <div className="space-y-6">
            <div className="flex items-center space-x-4">
              <FaEnvelope className="text-2xl text-blue-400" />
              <div>
                <p className="text-sm opacity-80">Email</p>
                <p className="font-medium">akankshabisht01@gmail.com</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <FaPhone className="text-2xl text-blue-400" />
              <div>
                <p className="text-sm opacity-80">Phone</p>
                <p className="font-medium">+91 XXXXXXXXXX</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <FaMapMarkerAlt className="text-2xl text-blue-400" />
              <div>
                <p className="text-sm opacity-80">Location</p>
                <p className="font-medium">Dehradun, Uttarakhand, India</p>
              </div>
            </div>
          </div>
        </div>
        <div>
          <h2 className="text-2xl font-semibold mb-6 text-green-300">Send a Message</h2>
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Name</label>
              <input
                type="text"
                className="w-full px-4 py-2 rounded bg-white/10 border border-white/20 focus:border-blue-500 focus:outline-none text-black"
                placeholder="Your name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                className="w-full px-4 py-2 rounded bg-white/10 border border-white/20 focus:border-blue-500 focus:outline-none text-black"
                placeholder="Your email"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Message</label>
              <textarea
                className="w-full px-4 py-2 rounded bg-white/10 border border-white/20 focus:border-blue-500 focus:outline-none h-32 text-black"
                placeholder="Your message"
              ></textarea>
            </div>
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-green-400 to-blue-500 hover:from-blue-500 hover:to-green-400 text-white font-bold py-2 px-4 rounded-xl shadow-lg transition-colors text-lg"
            >
              Send Message
            </button>
          </form>
        </div>
      </div>
    </div>
  );
} 