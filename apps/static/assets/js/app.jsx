import lens from "./assets/lens.png";
import "./App.css";

import React from 'react'

function App() {
  return (
    <div className="app">
      <div className="app-container">
        <div className="spotlight__wrapper">
          <input
            type="text"
            className="spotlight__input"
            placeholder="Ask me anything..."
            style={{
              backgroundImage: `url(${lens})`,
            }}
          />
          <div className="spotlight__answer">
            Dubai is a desert city and has a warm and sunny climate throughout
          </div>
        </div>
      </div>
      
    </div>
  );
}

export default App;
