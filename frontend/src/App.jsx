
import React, { useState } from "react";
import StrategyForm from "./components/StrategyForm";
import TradeLog from "./components/TradeLog";

function App() {
  const [result, setResult] = useState(null);
  const apiUrl = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

  const handleBacktest = async (params) => {
    const response = await fetch(`${apiUrl}/run-backtest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="App">
      <h1>Chris's Trading Tool</h1>
      <StrategyForm onRunBacktest={handleBacktest} />
      {result && (
        <div>
          <h2>Results</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      <TradeLog />
    </div>
  );
}

export default App;
