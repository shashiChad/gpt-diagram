import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import InputBox from './InputBox.jsx';
import GenerateButton from './GenerateButton.jsx';
import OutputBox from './OutputBox.jsx';
import Footer from './Footer.jsx';
export default function App () {
  const [input,setInput] = useState("");
  const [output, setOutput] = useState("");
  const navigate = useNavigate();

  const handleGenerate = () => {
    if (input.trim()) {
      setOutput(`Generated Diagram for: ${input}`);
      navigate("/diagram");
    } else {
      setOutput("⚠️ No input provided");
    }
  };


  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <main className="flex-grow p-6">
    <div className="w-full h-full bg-gray-800 rounded-2xl shadow-lg p-6 space-y-6 flex flex-col">
      {/* Title */}
      <h1 className="text-2xl font-bold">
         DiagramGPT 
      </h1>
      {/*Input*/}
      <InputBox
      input={input}
      setInput={setInput}
      />
      {/*Button*/}
      <div className="flex">
        <GenerateButton
        onGenerate={handleGenerate}
        />
      </div>
      
      {/*Output*/}
      <OutputBox
       output={output}
      />
            </div>
         
            </main>

      {/*Footer*/}
      <div className="max-w-5xl mx-auto">
         <Footer/>
      </div>
    </div>
  );
}

