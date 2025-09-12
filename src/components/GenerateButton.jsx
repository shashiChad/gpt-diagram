import React from "react";

export default function GenerateButton({ onGenerate }) {
  return (
    <button
      onClick={onGenerate}
      className="px-6 py-3 rounded-xl font-semibold text-white text-base
                 bg-gradient-to-r from-blue-600 to-purple-600
                 hover:from-blue-500 hover:to-purple-500
                 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-gray-900
                 shadow-lg transition-all duration-300"
    >
       Generate
    </button>
  );
}


