
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import InputBox from "./InputBox.jsx";
import GenerateButton from "./GenerateButton.jsx";

export default function Home() {
  const [input, setInput] = useState("");
  const navigate = useNavigate();

  const examples = [
    "Flow: Idea → Draft → Review → Publish",
    "Org: CEO → CTO → Dev Team; CEO → COO → Ops Team",
    "Mindmap: Project at center; Branches: Research, Design, Build, Launch"
  ];

  const handleGenerate = () => {
    if (input.trim()) {
      navigate("/diagram", { state: { input } });
    } else {
      alert("Please enter some text before generating!");
    }
  };

  const handleExampleClick = (example) => {
    setInput(example);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 text-white flex items-center justify-center p-6 fixed inset-0">
      <div className="w-full max-w-5xl mx-auto">
        {/* Main Card */}
        <div className="bg-gradient-to-br from-blue-900/40 to-purple-900/40 backdrop-blur-sm border border-blue-400/20 rounded-2xl shadow-2xl p-8 space-y-8">
          
          {/* Header Section */}
          <div className="space-y-4">
            <h1 className="text-4xl font-bold text-white leading-tight">
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Describe your diagram</span>
            </h1>
            <p className="text-lg text-gray-300 leading-relaxed">
              Type a short prompt. Use arrows (→) to connect steps, semicolons (;) for branches.
            </p>
          </div>

          {/* Input Section with Example */}
          <div className="space-y-6">
            <div className="relative">
              <InputBox 
                input={input} 
                setInput={setInput}
                placeholder="e.g. Flow: Idea → Draft → Review → Publish"
              />
            </div>
          </div>

          {/* Example Text Lines - Outside of input */}
          <div className="space-y-3 text-gray-400 text-base">
            <div 
              onClick={() => handleExampleClick(examples[0])}
              className="cursor-pointer hover:text-gray-300 transition-colors"
            >
              {examples[0]}
            </div>
            <div 
              onClick={() => handleExampleClick(examples[1])}
              className="cursor-pointer hover:text-gray-300 transition-colors"
            >
              {examples[1]}
            </div>
            <div 
              onClick={() => handleExampleClick(examples[2])}
              className="cursor-pointer hover:text-gray-300 transition-colors"
            >
              {examples[2]}
            </div>
          </div>

          {/* Generate Button Section */}
          <div className="flex justify-end">
            <GenerateButton onGenerate={handleGenerate} />
          </div>
        </div>
      </div>
    </div>
  );
}
