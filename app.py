"""
Ebola Contact Tracer - Flask REST API
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from tracer import (
    get_stats, get_infected, get_at_risk, get_infection_chain,
    get_country_spread, get_city_spread, get_super_spreaders,
    get_timeline, get_high_risk_events, get_graph,
    search_person, mark_infected, mark_quarantined, mark_recovered
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "project": "Ebola Contact Tracer",
        "version": "2.0",
        "region": "DRC · Uganda · Rwanda",
        "endpoints": [
            "/stats", "/infected", "/at-risk", "/chain",
            "/spread/country", "/spread/city", "/super-spreaders",
            "/timeline", "/high-risk-events", "/graph",
            "/search?name=...",
            "/mark/infected/<id>", "/mark/quarantined/<id>", "/mark/recovered/<id>"
        ]
    })

@app.route("/stats")
def stats():
    return jsonify(get_stats())

@app.route("/infected")
def infected():
    return jsonify(get_infected())

@app.route("/at-risk")
def at_risk():
    degrees = int(request.args.get("degrees", 2))
    return jsonify(get_at_risk(degrees))

@app.route("/chain")
def chain():
    start = request.args.get("from")
    end   = request.args.get("to")
    if not start or not end:
        return jsonify({"error": "Provide ?from=Name&to=Name"}), 400
    return jsonify(get_infection_chain(start, end))

@app.route("/spread/country")
def spread_country():
    return jsonify(get_country_spread())

@app.route("/spread/city")
def spread_city():
    return jsonify(get_city_spread())

@app.route("/super-spreaders")
def super_spreaders():
    return jsonify(get_super_spreaders())

@app.route("/timeline")
def timeline():
    return jsonify(get_timeline())

@app.route("/high-risk-events")
def high_risk_events():
    return jsonify(get_high_risk_events())

@app.route("/graph")
def graph():
    return jsonify(get_graph())

@app.route("/search")
def search():
    name = request.args.get("name", "")
    return jsonify(search_person(name))

@app.route("/mark/infected/<person_id>",    methods=["POST"])
def mark_inf(person_id):
    return jsonify(mark_infected(person_id))

@app.route("/mark/quarantined/<person_id>", methods=["POST"])
def mark_quar(person_id):
    return jsonify(mark_quarantined(person_id))

@app.route("/mark/recovered/<person_id>",   methods=["POST"])
def mark_rec(person_id):
    return jsonify(mark_recovered(person_id))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Ebola Tracer API running on http://localhost:{port}")
    app.run(debug=False, host="0.0.0.0", port=port)
