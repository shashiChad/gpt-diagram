import { useState } from 'react';
import {ClipboardCopy} from "lucide-react";

export default function OutputBox({ output }){
const [copied,setCopied] = useState(false);

const handleCopy = async () => {
  if(output) {
    await navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => 
      setCopied(false), 2000)
  }
};
  return (
    <div className="w-full rounded-xl bg-gray-800 border border-gray-600 shadow-lg overflow-hidden">
      {/*Header*/}
      <div className="bg-gray-700 px-4 py-2 border-b border-gray-600 flex items-center justify-between">
         <h2 className="text-sm md:text-base font-semibold text-gray-200">
           {output ? "Enhanced ouput" : "Awaiting input..."}
         </h2>

         {/*Copy Button*/}
         {output && (
          <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-gray-300 hover:text-white transition"
          >
             <ClipboardCopy 
             size={18}
             />
             <span className="hidden sm:inline text-sm">
               {copied ? "Copied!" : "Copy"}
             </span>
          </button>
         )}
      </div>
       
       {/*content area */}
       <div className="p-5 min-h-[180px] md:min-h-[220px] overflow-auto">
           {output ? (
            <p className="whitespace-pre-line text-base md:text-lg leading-relaxed text-gray-100">
              {output}
            </p>

           ):(
            <p className="text-gray-400 italic">
               Your enhaced text will appear here...
            </p>
           )}
       </div>
    </div>
  );
}


