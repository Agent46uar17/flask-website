from flask import Flask, jsonify
import requests

@app.route("/stats")
def stats():
    limits = requests.get(SERVER_URL, headers=HEADERS).json()
    res = requests.get(RESOURCES_URL, headers=HEADERS).json()

    mem_limit = limits["attributes"]["limits"]["memory"]
    disk_limit = limits["attributes"]["limits"]["disk"]

    r = res["attributes"]["resources"]

    return jsonify({
        "state": res["attributes"]["current_state"].upper(),
        "cpu": r["cpu_absolute"],
        "ram": r["memory_bytes"] / 1024 / 1024,
        "disk": r["disk_bytes"] / 1024 / 1024,
        "mem_limit": mem_limit,
        "disk_limit": disk_limit
    })