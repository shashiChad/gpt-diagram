// src/components/LandingPage.jsx
import React from "react";
import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-purple-700 via-indigo-800 to-blue-900 text-white px-6">
      <div className="text-center max-w-2xl">
        {/* Heading */}
        <h1 className="text-5xl font-extrabold mb-6">
          Welcome to <span className="text-purple-300"> Diagram Gpt</span>
        </h1>

        {/* Sub-heading */}
        <p className="text-lg text-gray-200 mb-8">
          Describe your ideas in plain text and instantly get beautiful, editable 
          diagrams. Drag, zoom, and export with ease.
        </p>

        {/* Buttons */}
        <div className="flex gap-4 justify-center">
          <Link
            to="/home"
            className="px-6 py-3 bg-purple-400 text-black font-semibold rounded-xl shadow-lg hover:bg-blue-300 transition"
          >
            Get Started
          </Link>

         <a
            
            
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 border border-white rounded-xl hover:bg-white hover:text-black transition"
          >
            Learn More
          </a>
        </div>
      </div>
    </div>
  );
}
