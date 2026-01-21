from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
import time

_last_data = None
_last_fetch = 0


app = Flask(__name__)
CORS(app)  # allow requests from WordPress


API_KEY = "ptlc_M7WDTQuHVtSSJGMIvzHzSefbIOmwsJHinbmjjUhsFut"
SERVER_ID = "77415725"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

SERVER_URL = f"https://gp.laag.in/api/client/servers/{SERVER_ID}"
RESOURCES_URL = f"{SERVER_URL}/resources"


@app.route("/")
def home():
    return "LootBot API is running"

@app.route("/stats")
def stats():
    global _last_data, _last_fetch

    # cache for 3 seconds
    if _last_data and time.time() - _last_fetch < 3:
        return jsonify(_last_data)

    try:
        limits = requests.get(SERVER_URL, headers=HEADERS, timeout=5).json()
        res = requests.get(RESOURCES_URL, headers=HEADERS, timeout=5).json()

        mem_limit = limits["attributes"]["limits"]["memory"]
        disk_limit = limits["attributes"]["limits"]["disk"]

        r = res["attributes"]["resources"]

        data = {
            "state": res["attributes"]["current_state"].upper(),
            "cpu": round(r["cpu_absolute"], 1),
            "ram": round(r["memory_bytes"] / 1024 / 1024, 1),
            "disk": round(r["disk_bytes"] / 1024 / 1024, 1),
            "mem_limit": mem_limit,
            "disk_limit": disk_limit,
            "rx": round(r["network_rx_bytes"] / 1024 / 1024, 1),
            "tx": round(r["network_tx_bytes"] / 1024 / 1024, 1),
            "ts": int(time.time())  # timestamp (for debugging)
        }

        _last_data = data
        _last_fetch = time.time()

        return jsonify(data)

    except Exception:
        return jsonify({"state": "OFFLINE"}), 500



# ================== RUN ==================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
