import { useNavigate } from "react-router-dom";
import SearchBar from "../components/SearchBar";
import ChatBot from "../components/ChatBot";
import OcrCamera from "../components/OcrCamera";
import "../css/Home.css";
import "../css/Navbar.css";

function Home() {
  const navigate = useNavigate();

  return (
    <>
      <div className="navbar">MediLens</div>

      <div className="home-container">
        <SearchBar onSearch={(q) => navigate(`/medicine/${q}`)} />

        <div className="options">
          <ChatBot />

          {/* 🔥 OCR RESULT HANDLER */}
          <OcrCamera
            onResult={(data) => {
              console.log("OCR RESULT:", data);

              if (data?.drug_names?.length > 0) {
                navigate(`/medicine/${data.drug_names[0]}`);
              }
            }}
          />
        </div>
      </div>
    </>
  );
}

export default Home;
