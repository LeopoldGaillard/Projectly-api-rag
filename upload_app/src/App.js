import logo from "./logo.webp";
import "./App.css";
import React from "react";
import FileUpload from "./FileUpload";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
      </header>

      <div className="App">
        <h1>Add your doc</h1>
        <FileUpload />
      </div>
    </div>
  );
}

export default App;
