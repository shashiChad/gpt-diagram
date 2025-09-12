
import React from "react";

export default function InputBox({ input, setInput }) {
  return (
    <textarea
      value={input}
      onChange={(e) => setInput(e.target.value)}
      placeholder="Describe your diagram..."
      className="w-full h-48 p-4 rounded-xl 
                 bg-gradient-to-br from-gray-900 via-purple-700 to-blue-900
                 border border-gray-700 text-white
                 font-mono text-sm resize-none
                 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-lg"
    />
  );
}

