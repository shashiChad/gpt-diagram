import React from 'react'
export default function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-300 py-6 px-6 mt-6 rounded-t-2xl">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-10">
        <div>
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 bg-gradient-to-r from-blue-500 to-blue-500 rounded-sm"></div>
            <span className="text-lg font-semibold">E-skillveda</span>
          </div>
          <p className="text-sm mt-2 text-gray-400">
            Documents & diagrams <br /> for engineering teams
          </p>
        </div>

        {/* Use Cases */}
        <div>
          <h3 className="text-gray-400 text-sm font-semibold mb-3">Use Cases</h3>
          <ul className="space-y-2 text-sm">
            <li>Architecture Diagrams</li>
            <li>Design Docs</li>
            <li>Documentation</li>
            <li>Brainstorming</li>
            <li>Wireframes</li>
            <li>Whiteboard Interview</li>
          </ul>
        </div>

        {/* Resources */}
        <div>
          <h3 className="text-gray-400 text-sm font-semibold mb-3">Resources</h3>
          <ul className="space-y-2 text-sm">
            <li> Examples</li>
            <li>Decision Node</li>
            <li>Guides</li>
            <li>DiagramGPT</li>
            <li>Free Diagram Maker</li>
            <li>Docs →</li>
            <li>DesignDocs.dev →</li>
          </ul>
        </div>

        {/* Free Diagram Makers */}
        <div>
          <h3 className="text-gray-400 text-sm font-semibold mb-3">Free Diagram Makers</h3>
          <ul className="space-y-2 text-sm">
            <li>Architecture Diagrams</li>
            <li>Data Flow Diagrams</li>
            <li>Sequence Diagrams</li>
            <li>Network Diagrams</li>
            <li>Flowcharts</li>
            <li>ERDs</li>
          </ul>
        </div>

        {/* About */}
        <div>
          <h3 className="text-gray-400 text-sm font-semibold mb-3">About</h3>
          <ul className="space-y-2 text-sm">
            <li>Pricing</li>
            <li>AI</li>
            <li>Team</li>
            <li>Slack Community →</li>
            <li>Careers →</li>
            <li>Privacy Policy</li>
            <li>Terms</li>
            <li className="border border-gray-600 px-3 py-1 rounded-md inline-block">
               Editor
            </li>
          </ul>
        </div>
      </div>

      {/* Bottom */}
      <div className="mt-10 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
        <p>© 2025 E-skillveda, Inc.</p>
        <div className="flex space-x-4 mt-4 md:mt-0">
          <a href="#" className="hover:text-white">🐦</a>
          <a href="#" className="hover:text-white"><i class="fa fa-linkedin-square"></i></a>
        </div>
      </div>
    </footer>
  );
}
