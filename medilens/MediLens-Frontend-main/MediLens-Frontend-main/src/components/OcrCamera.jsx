import { useRef, useState } from "react";
import "../css/OcrCamera.css";

function OcrCamera({ onResult }) {
  const fileInputRef = useRef(null);
  const [file, setFile] = useState(null);

  const handleCardClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/api/ocr", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("OCR RESPONSE:", data);

    if (onResult) {
      onResult(data);
    }
  };

  return (
    <div className="ocr-card">
      <h3>OCR Camera</h3>

      <div className="upload-box" onClick={handleCardClick}>
        <span className="camera-icon">📷</span>
        <p>Click the camera to upload an image</p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        hidden
        onChange={handleFileChange}
      />

      {file && (
        <button className="scan-btn" onClick={handleUpload}>
          Scan Medicine
        </button>
      )}
    </div>
  );
}

export default OcrCamera;
