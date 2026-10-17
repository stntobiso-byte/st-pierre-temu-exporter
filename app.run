
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({
        "app": "St Pierre Temu exporter",
        "status": "running",
        "message": "Web service is online. Shopify is not connected yet."
    })

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
