import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import MedicinePage from "./pages/MedicinePage";
import "./css/App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/medicine/:name" element={<MedicinePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
