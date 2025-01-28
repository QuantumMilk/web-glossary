import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Glossary from './pages/Glossary';
import Graph from './pages/Graph';
import Admin from './pages/Admin';
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <div className="navbar">
          <Link to="/glossary">Глоссарий</Link>
          <Link to="/graph">Семантический граф</Link>
          <Link to="/admin">Админ</Link>
        </div>
        <Routes>
          <Route path="/" element={<Glossary />} />
          <Route path="/glossary" element={<Glossary />} />
          <Route path="/graph" element={<Graph />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
