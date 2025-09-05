import React from "react";
import DiagramSection from "./components/DiagramSection.jsx"
import Home from "./components/Home.jsx";
import { Routes, Route } from "react-router-dom";

export default function App(){
    return(
        <Routes>
            <Route
            path="/" element={<Home/>} />
            <Route
            className="bg-blue-500"
            path="/diagram" element={<DiagramSection/>}
            />
            
        </Routes>
    );
}