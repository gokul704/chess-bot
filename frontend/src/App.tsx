import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState("Loading...");

  useEffect(() => {
    fetch("http://localhost:8000/health")
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch((err) => {
        console.error(err);
        setStatus("Backend not reachable");
      });
  }, []);

  return (
    <div>
      <h1>Chess Mentor AI</h1>
      <h2>Backend Status</h2>
      <p>{status}</p>
    </div>
  );
}

export default App;