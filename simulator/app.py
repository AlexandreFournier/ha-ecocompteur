"""
Ecocompteur API Simulator.

A simple HTTP server that simulates the Ecocompteur API
for testing purposes.
"""

import json
import random
import time
from datetime import UTC, datetime

from flask import Flask, Response

app = Flask(__name__)


def get_current_power() -> float:
    """Generate realistic varying power consumption."""
    base = 200
    variation = random.uniform(-50, 100)  # noqa: S311
    return round(base + variation, 2)


@app.route("/data.json")
def data_json() -> Response:
    """Serve the general configuration and consumption data."""
    data = {
        "option_tarifaire": 4,
        "tarif_courant": 11,
        "isousc": 0,
        "conso_base": 0,
        "conso_hc": 1234567,
        "conso_hp": 2345678,
        "conso_hc_b": 0,
        "conso_hp_b": 0,
        "conso_hc_w": 0,
        "conso_hp_w": 0,
        "conso_hc_r": 0,
        "conso_hp_r": 0,
        "type_imp_0": 1,
        "type_imp_1": 1,
        "type_imp_2": 1,
        "type_imp_3": 1,
        "type_imp_4": 1,
        "type_imp_5": 1,
        "label_entree1": "Consommation globale",
        "label_entree2": "Cumulus             ",
        "label_entree3": "Cuisine             ",
        "label_entree4": "Prises de Courant",
        "label_entree5": "Informatique        ",
        "label_entree_imp0": "Eau",
        "label_entree_imp1": "Gaz",
        "label_entree_imp2": "Eau Chaude",
        "label_entree_imp3": "Chauffage",
        "label_entree_imp4": "Climatisation",
        "label_entree_imp5": "Piscine",
        "entree_imp0_disabled": 0,
        "entree_imp1_disabled": 1,
        "entree_imp2_disabled": 1,
        "entree_imp3_disabled": 1,
        "entree_imp4_disabled": 1,
        "entree_imp5_disabled": 1,
    }
    return Response(json.dumps(data), mimetype="application/json")


@app.route("/inst.json")
def inst_json() -> Response:
    """Serve real-time instantaneous data with dynamic values."""
    now = datetime.now(tz=UTC)
    data = {
        "data1": get_current_power(),
        "data2": round(random.uniform(0, 50), 2),  # noqa: S311
        "data3": round(random.uniform(0, 30), 2),  # noqa: S311
        "data4": round(random.uniform(0, 20), 2),  # noqa: S311
        "data5": round(random.uniform(50, 100), 2),  # noqa: S311
        "data6": round(random.uniform(60, 70), 6),  # noqa: S311
        "data6m3": round(random.uniform(60, 70), 6),  # noqa: S311
        "data7": 0.0,
        "data7m3": 0.0,
        "heure": now.hour,
        "minute": now.minute,
        "CIR1_Nrj": round(random.uniform(0, 10), 6),  # noqa: S311
        "CIR1_Vol": round(random.uniform(0, 5), 6),  # noqa: S311
        "CIR2_Nrj": 0.0,
        "CIR2_Vol": 0.0,
        "CIR3_Nrj": 0.0,
        "CIR3_Vol": 0.0,
        "CIR4_Nrj": 0.0,
        "CIR4_Vol": 0.0,
        "Date_Time": int(time.time()),
    }
    return Response(json.dumps(data), mimetype="application/json")


@app.route("/log1.csv")
def log1_csv() -> Response:
    """Serve statistics in CSV format."""
    header = (
        "Date,Heure,Circuit1,Circuit2,Circuit3,"
        "Circuit4,Circuit5,TIC1,TIC2,TIC3,TIC4,TIC5,TIC6"
    )
    rows = [
        "2026-02-13,00:00,123.45,45.67,23.45,12.34,56.78,1.23,2.34,3.45,4.56,5.67,6.78",
        "2026-02-13,01:00,134.56,46.78,24.56,13.45,57.89,1.34,2.45,3.56,4.67,5.78,6.89",
        "2026-02-13,02:00,125.67,44.56,22.34,11.23,55.67,1.25,2.36,3.47,4.58,5.69,6.70",
        "2026-02-13,03:00,115.78,42.34,20.12,10.11,53.45,1.15,2.26,3.37,4.48,5.59,6.60",
        "2026-02-13,04:00,120.89,43.45,21.23,11.34,54.56,1.20,2.31,3.42,4.53,5.64,6.75",
    ]
    csv_data = header + "\n" + "\n".join(rows) + "\n"
    return Response(csv_data, mimetype="text/csv")


@app.route("/log2.csv")
def log2_csv() -> Response:
    """Serve additional statistics in CSV format."""
    header = (
        "Date,Circuit1_Total,Circuit2_Total,Circuit3_Total,"
        "Circuit4_Total,Circuit5_Total,Water_Total,Gas_Total"
    )
    rows = [
        "2026-02-01,3456.78,1234.56,567.89,234.56,890.12,123.45,45.67",
        "2026-02-02,3478.90,1245.67,578.90,245.67,901.23,124.56,46.78",
        "2026-02-03,3501.23,1256.78,589.01,256.78,912.34,125.67,47.89",
        "2026-02-04,3523.45,1267.89,600.12,267.89,923.45,126.78,48.90",
        "2026-02-05,3545.67,1278.90,611.23,278.90,934.56,127.89,49.01",
    ]
    csv_data = header + "\n" + "\n".join(rows) + "\n"
    return Response(csv_data, mimetype="text/csv")


@app.route("/")
def index() -> str:
    """Serve a simple index page with available endpoints."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ecocompteur API Simulator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            .endpoint {
                background: #f4f4f4;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
            }
            a {
                color: #0066cc;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Ecocompteur API Simulator</h1>
        <p>This simulator provides the Ecocompteur API
        for testing purposes.</p>
        <h2>Available Endpoints:</h2>
        <div class="endpoint">
            <strong><a href="/data.json">/data.json</a></strong>
            - General configuration and consumption data
        </div>
        <div class="endpoint">
            <strong><a href="/inst.json">/inst.json</a></strong>
            - Real-time instantaneous data (updates dynamically)
        </div>
        <div class="endpoint">
            <strong><a href="/log1.csv">/log1.csv</a></strong>
            - Hourly statistics (CSV format)
        </div>
        <div class="endpoint">
            <strong><a href="/log2.csv">/log2.csv</a></strong>
            - Daily statistics (CSV format)
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)  # noqa: S201, S104
