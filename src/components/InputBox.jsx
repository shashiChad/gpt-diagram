import React from 'react'

export default function InputBox({input, setInput}) {
  return (
    <textarea
     value={input}
     onChange={(e) => 
        setInput(e.target.value)}
    placeholder="Describe your diagram..."
    className="w-full h-32 p-3 rounded-lg bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-blue-500"
    />
  );
}

