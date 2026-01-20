from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# ================== CONFIG ==================

API_KEY = "PUT_YOUR_PTERODACTYL_API_KEY_HERE"
SERVER_ID = "77415725"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

SERVER_URL = f"https://gp.laag.in/api/client/servers/{SERVER_ID}"
RESOURCES_URL = f"{SERVER_URL}/resources"

# ================== ROUTES ==================

# Main website
@app.route("/")
def home():
    return render_template("index.html")

# Live stats API (used by website JS)
@app.route("/stats")
def stats():
    try:
        limits = requests.get(SERVER_URL, headers=HEADERS, timeout=3).json()
        res = requests.get(RESOURCES_URL, headers=HEADERS, timeout=3).json()

        mem_limit = limits["attributes"]["limits"]["memory"]
        disk_limit = limits["attributes"]["limits"]["disk"]

        r = res["attributes"]["resources"]

        return jsonify({
            "state": res["attributes"]["current_state"].upper(),
            "cpu": r["cpu_absolute"],
            "ram": r["memory_bytes"] / 1024 / 1024,
            "disk": r["disk_bytes"] / 1024 / 1024,
            "mem_limit": mem_limit,
            "disk_limit": disk_limit,
            "rx": r["network_rx_bytes"] / 1024 / 1024,
            "tx": r["network_tx_bytes"] / 1024 / 1024
        })

    except Exception as e:
        return jsonify({"error": "offline"}), 500


# ================== RUN ==================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)