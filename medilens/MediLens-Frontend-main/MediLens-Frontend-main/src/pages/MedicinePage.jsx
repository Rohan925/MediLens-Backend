import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "../css/MedicinePage.css";

function MedicinePage() {
  const { name } = useParams();
  const [drugInfo, setDrugInfo] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/drug/${name}`)
      .then((res) => res.json())
      .then((data) => setDrugInfo(data));
  }, [name]);

  return (
    <div className="medicine-page">
      <h2>Medicine Information</h2>

      <div className="card-grid">
        {drugInfo.map((drug, index) => (
          <div className="drug-card" key={index}>
            <h3>{drug.name}</h3>
            <p>{drug.description || "No description available"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MedicinePage;
