
import React, { useState } from "react";

function StrategyForm({ onRunBacktest }) {
  const [ticker, setTicker] = useState("AAPL");
  const [start, setStart] = useState("2023-01-01");
  const [end, setEnd] = useState("2024-01-01");

  const handleSubmit = (e) => {
    e.preventDefault();
    onRunBacktest({ ticker, start, end });
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Ticker: <input value={ticker} onChange={(e) => setTicker(e.target.value)} /></label>
      <label>Start Date: <input type="date" value={start} onChange={(e) => setStart(e.target.value)} /></label>
      <label>End Date: <input type="date" value={end} onChange={(e) => setEnd(e.target.value)} /></label>
      <button type="submit">Run Backtest</button>
    </form>
  );
}

export default StrategyForm;
