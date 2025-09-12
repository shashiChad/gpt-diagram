import React from "react";
import { Routes, Route } from "react-router-dom";
import LandingPage from "./components/landingpage.jsx";
import Home from "./components/Home.jsx";
import DiagramSection from "./components/DiagramSection.jsx";

export default function App() {
  return (
    <Routes>
      {/* Landing Page at "/" */}
      <Route path="/" element={<LandingPage />} />

      {/* Home Page */}
      <Route path="/home" element={<Home />} />

      {/* Diagram Section */}
      <Route path="/diagram" element={<DiagramSection />} />
    </Routes>
  );
}



