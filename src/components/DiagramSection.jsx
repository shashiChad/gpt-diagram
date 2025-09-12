
import { useEffect, useRef, useState, useId } from "react";
import { Link } from "react-router-dom";
import mermaid from "mermaid";

// Simple debounce hook
function useDebounce(value, delay = 500) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debounced;
}

export default function DiagramSection() {
  const [diagramCode, setDiagramCode] = useState(`graph TD
A[Start] --> B[Do Something]
B --> C{Condition?}
C -->|Yes| D[Option 1]
C -->|No| E[Option 2]`);

  const [svgContent, setSvgContent] = useState(null);
  const [error, setError] = useState(null);

  const diagramId = useId(); // unique ID per component
  const debouncedCode = useDebounce(diagramCode, 400); // debounce keystrokes

  // Initialize Mermaid once
  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: "dark" });
  }, []);

  // Render Mermaid when code changes (debounced)
  useEffect(() => {
    setError(null);
    setSvgContent(null);

    mermaid
      .render(`diagram-${diagramId}`, debouncedCode)
      .then(({ svg }) => {
        setSvgContent(svg);
      })
      .catch((err) => {
        setError(err.message || "⚠️ Error in Mermaid code");
      });
  }, [debouncedCode, diagramId]);

  return (
    <div className="min-h-screen flex flex-col bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gray-800 px-6 py-4 border-b border-gray-700">
        <h1 className="text-lg md:text-xl font-bold">📊 Diagram Editor</h1>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: Editor */}
        <textarea
          value={diagramCode}
          onChange={(e) => setDiagramCode(e.target.value)}
          className="flex-1 p-4 bg-gray-950 text-white font-mono text-sm 
                     resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Write Mermaid diagram code here..."
        />

        {/* Right: Preview */}
        <div className="flex-1 flex items-center justify-center bg-gray-950 border-l border-gray-700 overflow-auto p-4">
          {error ? (
            <p className="text-red-400">{error}</p>
          ) : svgContent ? (
            <div
              className="max-w-full max-h-full"
              dangerouslySetInnerHTML={{ __html: svgContent }}
            />
          ) : (
            <p className="text-gray-400">Rendering diagram...</p>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 flex justify-center">
        <Link
          to="/"
          className="px-6 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition"
        >
           Back to Home
        </Link>
      </div>
    </div>
  );
}
