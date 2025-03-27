
from flask import Flask, request, jsonify
from strategies.src_strategy import run_src_strategy
import os

app = Flask(__name__)

@app.route("/run-backtest", methods=["POST"])
def run_backtest():
    params = request.json
    results = run_src_strategy(params)
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
