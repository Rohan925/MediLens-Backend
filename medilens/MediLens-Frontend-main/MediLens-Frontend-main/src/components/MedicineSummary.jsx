import { useEffect, useState } from "react";

export default function MedicineSummary({ medicineName }) {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!medicineName) return;

    const fetchSummary = async () => {
      setLoading(true);
      setError("");

      try {
        const res = await fetch(
          "http://localhost:8000/api/medicine/summary",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              medicine: medicineName,
            }),
          }
        );

        if (!res.ok) {
          throw new Error("Failed to fetch summary");
        }

        const data = await res.json();
        setSummary(data.summary);
      } catch (err) {
        setError("Failed to load medicine summary.");
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, [medicineName]); // ✅ dependency array MUST be here

  if (loading) return <p>Loading medicine summary...</p>;
  if (error) return <p>{error}</p>;

  return <p>{summary}</p>;
}
