import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import mermaid from "mermaid";

export default function DiagramSection() {
  const [diagramCode, setDiagramCode] = useState(`graph TD
A[Start] --> B[Do Something]
B --> C{Condition?}
C -->|Yes| D[Option 1]
C -->|No| E[Option 2]`);

  const diagramRef = useRef(null);

  useEffect(() => {
    if (diagramRef.current) {
      try {
        // Clear old content before re-render
        diagramRef.current.innerHTML = "";

        // Initialize Mermaid
        mermaid.initialize({ startOnLoad: false, theme: "dark" });

        // Render the diagram
        mermaid.render("theDiagram", diagramCode, (svgCode) => {
          diagramRef.current.innerHTML = svgCode;
        });
      } catch (err) {
        diagramRef.current.innerHTML =
          "<p class='text-red-400'>⚠️ Error in Mermaid code</p>";
      }
    }
  }, [diagramCode]); // Runs every time code changes

  return (
    <div className="w-full bg-gray-800 border border-gray-600 rounded-xl shadow-lg overflow-hidden mt-8">
      {/* Header */}
      <div className="bg-gray-700 px-4 py-2 border-b border-gray-600">
        <h2 className="text-sm md:text-base font-semibold text-gray-200">
          📊 Diagram Editor
        </h2>
      </div>

      {/* Grid: Editor + Preview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
        {/* Left: Code Editor */}
        <textarea
          value={diagramCode}
          onChange={(e) => setDiagramCode(e.target.value)}
          className="w-full min-h-[250px] p-4 rounded-lg bg-gray-900 text-white
                     font-mono text-sm resize-y focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Write Mermaid diagram code here..."
        />

        {/* Right: Diagram Render */}
        <div className="flex flex-col items-center gap-4">
          <div
            ref={diagramRef}
            className="w-full min-h-[250px] bg-gray-900 rounded-lg border border-gray-700 flex items-center justify-center"
          >
            <p className="text-gray-400">Rendering diagram...</p>
          </div>

          
        </div>
      </div>
      <Link
        to="/"
        className="mt-6 px-6 py-2 bg-blue-600 rounded-lg hover:bg-blue-700"
      >
        ⬅ Back to Home
      </Link>
    </div>
  );
}
