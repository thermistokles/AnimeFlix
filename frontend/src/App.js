import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Register from './components/Register/Register';

function App() {
  return (
    <div className="App">
      <Register />
    </div>
  );
}

export default App;
