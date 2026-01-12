import { useState } from "react";

export default function OcrCamera() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://localhost:8000/api/ocr", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("OCR request failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("OCR failed. Please try another image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tool-card">
      <div className="tool-header">OCR Camera</div>

      {/* Camera clickable area */}
      <div className="tool-body tool-camera">
        <label className="camera-button">
          📷
          <input
            type="file"
            accept="image/*"
            hidden
            onChange={handleFileChange}
          />
        </label>
      </div>

      {/* Footer / Result area */}
      <div className="tool-footer">
        {loading && <span className="ocr-hint">Scanning image...</span>}

        {error && (
          <span className="ocr-hint" style={{ color: "red" }}>
            {error}
          </span>
        )}

        {!loading && !result && !error && (
          <span className="ocr-hint">
            Click the camera to upload an image
          </span>
        )}

        {result?.detected_drug && (
          <div className="ocr-hint">
            <b>Detected:</b> {result.detected_drug}
          </div>
        )}
      </div>
    </div>
  );
}
