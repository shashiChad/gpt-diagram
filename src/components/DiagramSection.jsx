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
        diagramRef.current.innerHTML = "";
        mermaid.initialize({ startOnLoad: false, theme: "dark" });

        mermaid
          .render("theDiagram", diagramCode)
          .then(({ svg }) => {
            if (diagramRef.current) {
              diagramRef.current.innerHTML = svg;
            }
          })
          .catch(() => {
            if (diagramRef.current) {
              diagramRef.current.innerHTML =
                "<p class='text-red-400'>⚠️ Error in Mermaid code</p>";
            }
          });
      } catch (err) {
        if (diagramRef.current) {
          diagramRef.current.innerHTML =
            "<p class='text-red-400'>⚠️ Error in Mermaid code</p>";
        }
      }
    }
  }, [diagramCode]);

  return (
    <div className="min-h-screen flex flex-col bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gray-800 px-6 py-4 border-b border-gray-700">
        <h1 className="text-lg md:text-xl font-bold">📊 Diagram Editor</h1>
      </div>

      {/* Main Content: full screen split */}
      <div className="flex flex-1">
        {/* Left: Editor */}
        <textarea
          value={diagramCode}
          onChange={(e) => setDiagramCode(e.target.value)}
          className="flex-1 p-4 bg-gray-950 text-white font-mono text-sm 
                     resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Write Mermaid diagram code here..."
        />

        {/* Right: Preview */}
        <div className="flex-1 flex items-center justify-center bg-gray-950 border-l border-gray-700">
          <div
            ref={diagramRef}
            className="w-full h-full flex items-center justify-center"
          >
            <p className="text-gray-400">Rendering diagram...</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className=" p-4  flex justify-center">
        <Link
          to="/"
          className="px-6 py-2 bg-blue-600 rounded-lg hover:bg-blue-700"
        >
          ⬅ Back to Home
        </Link>
      </div>
    </div>
  );
}
