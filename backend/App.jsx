import React, { useState } from "react";

export default function App() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");

  const askAgent = async () => {
    const res = await fetch("http://localhost:8000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input }),
    });
    const data = await res.json();
    setOutput(data.response);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Life Annuity Advisor</h1>
      <textarea rows={5} value={input} onChange={e => setInput(e.target.value)} />
      <br />
      <button onClick={askAgent}>Submit</button>
      <pre>{output}</pre>
    </div>
  );
}
