import React, { useState } from "react";

export default function App() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const askAgent = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      });
      const data = await res.json();
      setOutput(data.response);
    } catch (error) {
      setOutput("Error: Could not connect to backend server. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      askAgent();
    }
  };

  return (
    <div style={{
      padding: "2rem",
      maxWidth: "800px",
      margin: "0 auto",
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      gap: "1.5rem"
    }}>
      <div style={{
        background: "rgba(255, 255, 255, 0.95)",
        borderRadius: "20px",
        padding: "2rem",
        boxShadow: "0 20px 40px rgba(0,0,0,0.1)",
        backdropFilter: "blur(10px)"
      }}>
        <h1 style={{
          color: "#333",
          textAlign: "center",
          marginBottom: "0.5rem",
          fontSize: "2.5rem",
          fontWeight: "600"
        }}>
          🏦 Life Annuity Advisor
        </h1>
        <p style={{
          textAlign: "center",
          color: "#666",
          marginBottom: "2rem",
          fontSize: "1.1rem"
        }}>
          Get personalized annuity recommendations powered by AI
        </p>

        <div style={{ marginBottom: "1.5rem" }}>
          <label style={{
            display: "block",
            marginBottom: "0.5rem",
            fontWeight: "500",
            color: "#333"
          }}>
            Tell us about your retirement goals and financial situation:
          </label>
          <textarea
            rows={6}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Example: I'm 67 years old, recently retired, and looking for guaranteed income. I prefer low-risk investments and want to ensure steady monthly payments for life..."
            style={{
              width: "100%",
              padding: "1rem",
              border: "2px solid #e0e0e0",
              borderRadius: "10px",
              fontSize: "1rem",
              fontFamily: "inherit",
              resize: "vertical",
              outline: "none",
              transition: "border-color 0.3s ease",
              boxSizing: "border-box"
            }}
            onFocus={e => e.target.style.borderColor = "#667eea"}
            onBlur={e => e.target.style.borderColor = "#e0e0e0"}
          />
          <div style={{
            fontSize: "0.9rem",
            color: "#666",
            marginTop: "0.5rem",
            textAlign: "right"
          }}>
            Press Ctrl+Enter to submit
          </div>
        </div>

        <button
          onClick={askAgent}
          disabled={loading || !input.trim()}
          style={{
            width: "100%",
            padding: "1rem 2rem",
            backgroundColor: loading || !input.trim() ? "#ccc" : "#667eea",
            color: "white",
            border: "none",
            borderRadius: "10px",
            fontSize: "1.1rem",
            fontWeight: "600",
            cursor: loading || !input.trim() ? "not-allowed" : "pointer",
            transition: "all 0.3s ease",
            transform: loading ? "scale(0.98)" : "scale(1)"
          }}
        >
          {loading ? "🔄 Analyzing your profile..." : "🎯 Get My Recommendation"}
        </button>
      </div>

      {output && (
        <div style={{
          background: "rgba(255, 255, 255, 0.95)",
          borderRadius: "20px",
          padding: "2rem",
          boxShadow: "0 20px 40px rgba(0,0,0,0.1)",
          backdropFilter: "blur(10px)"
        }}>
          <h2 style={{
            color: "#333",
            marginBottom: "1rem",
            fontSize: "1.5rem",
            fontWeight: "600"
          }}>
            📋 Your Personalized Recommendation
          </h2>
          <pre style={{
            whiteSpace: "pre-wrap",
            fontFamily: "inherit",
            fontSize: "1rem",
            lineHeight: "1.6",
            color: "#333",
            margin: 0,
            background: "#f8f9fa",
            padding: "1.5rem",
            borderRadius: "10px",
            border: "1px solid #e9ecef"
          }}>
            {output}
          </pre>
        </div>
      )}
    </div>
  );
}
