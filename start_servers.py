"""Script de démarrage des services PointSetManager (port 5000) et Triangulator (port 5001).

Usage (cmd.exe):
  python start_servers.py manager
  python start_servers.py triangulator
  python start_servers.py both
"""

import sys
import uuid
import threading
from typing import Dict
from flask import Flask, request, jsonify, make_response
import requests

from TP.modules.PointSet import PointSet
from TP.modules.Triangulation import Triangulation

# --- PointSetManager ---
manager_app = Flask("pointset_manager")
_STORAGE: Dict[str, bytes] = {}

@manager_app.post("/pointset")
def register_pointset():
    data = request.get_data()
    try:
        # validation du format
        _ = PointSet.from_binary(data)
    except Exception as e:
        return jsonify({"code": "BAD_FORMAT", "message": str(e)}), 400
    ps_id = str(uuid.uuid4())
    _STORAGE[ps_id] = data
    return jsonify({"pointSetId": ps_id}), 201

@manager_app.get("/pointset/<point_set_id>")
def get_pointset(point_set_id: str):
    # Validation UUID
    try:
        uuid.UUID(point_set_id)
    except ValueError:
        return jsonify({"code": "BAD_ID", "message": "Format UUID invalide"}), 400
    raw = _STORAGE.get(point_set_id)
    if raw is None:
        return jsonify({"code": "NOT_FOUND", "message": "PointSet introuvable"}), 404
    resp = make_response(raw)
    resp.headers["Content-Type"] = "application/octet-stream"
    return resp

# --- Triangulator ---
triangulator_app = Flask("triangulator")
MANAGER_URL = "http://127.0.0.1:5000"

@triangulator_app.get("/triangulation/<point_set_id>")
def get_triangulation(point_set_id: str):
    try:
        uuid.UUID(point_set_id)
    except ValueError:
        return jsonify({"code": "BAD_ID", "message": "Format UUID invalide"}), 400
    # Récupérer point set du manager
    try:
        r = requests.get(f"{MANAGER_URL}/pointset/{point_set_id}")
    except requests.exceptions.RequestException as e:
        return jsonify({"code": "MANAGER_UNAVAILABLE", "message": str(e)}), 503
    if r.status_code == 404:
        return jsonify({"code": "NOT_FOUND", "message": "PointSet introuvable"}), 404
    if r.status_code != 200:
        return jsonify({"code": "UPSTREAM_ERROR", "message": f"Manager status {r.status_code}"}), 503
    try:
        ps = PointSet.from_binary(r.content)
    except Exception as e:
        return jsonify({"code": "BAD_UPSTREAM_DATA", "message": str(e)}), 500
    # Construire triangulation (éventail naïf)
    tri = Triangulation.depuis_ensemble_eventail(ps)
    binary = tri.to_binary()
    resp = make_response(binary)
    resp.headers["Content-Type"] = "application/octet-stream"
    return resp


def run_manager():
    manager_app.run(host="127.0.0.1", port=5000)

def run_triangulator():
    triangulator_app.run(host="127.0.0.1", port=5001)


def main():
    if len(sys.argv) < 2:
        print("Argument requis: manager | triangulator | both")
        sys.exit(1)
    mode = sys.argv[1].lower()
    if mode == "manager":
        run_manager()
    elif mode == "triangulator":
        run_triangulator()
    elif mode == "both":
        t1 = threading.Thread(target=run_manager, daemon=True)
        t2 = threading.Thread(target=run_triangulator, daemon=True)
        t1.start(); t2.start()
        print("Services démarrés. CTRL+C pour arrêter.")
        t1.join(); t2.join()
    else:
        print("Mode inconnu.")
        sys.exit(1)

if __name__ == "__main__":
    main()
