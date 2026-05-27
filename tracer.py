"""
Ebola Contact Tracer - Neo4j Query Engine
All graph queries powering the API
"""
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

_uri  = os.getenv("NEO4J_URI")
_user = os.getenv("NEO4J_USERNAME")
_pass = os.getenv("NEO4J_PASSWORD")

if not _uri or not _user or not _pass:
    missing = [k for k, v in {
        "NEO4J_URI": _uri, "NEO4J_USERNAME": _user, "NEO4J_PASSWORD": _pass
    }.items() if not v]
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing)}. "
        "Set them in your deployment platform's environment settings."
    )

driver = GraphDatabase.driver(_uri, auth=(_user, _pass))
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def _run(query, **params):
    with driver.session(database=DATABASE) as s:
        return [dict(r) for r in s.run(query, **params)]


# ── Dashboard stats ──────────────────────────────────────────────────────────

def get_stats():
    rows = _run("""
        MATCH (p:Person)
        RETURN
          COUNT(p)                                           AS total,
          SUM(CASE WHEN p.infected  THEN 1 ELSE 0 END)      AS infected,
          SUM(CASE WHEN p.deceased  THEN 1 ELSE 0 END)      AS deceased,
          SUM(CASE WHEN p.recovered THEN 1 ELSE 0 END)      AS recovered,
          SUM(CASE WHEN p.quarantined THEN 1 ELSE 0 END)    AS quarantined,
          COUNT(DISTINCT p.country)                         AS countries_affected
    """)
    stats = rows[0] if rows else {}

    at_risk = _run("""
        MATCH (infected:Person {infected: true})-[:MET]-(atRisk:Person)
        WHERE atRisk.infected = false AND atRisk.deceased = false
        RETURN COUNT(DISTINCT atRisk) AS at_risk
    """)
    stats["at_risk"] = at_risk[0]["at_risk"] if at_risk else 0
    return stats


# ── Infected people ──────────────────────────────────────────────────────────

def get_infected():
    return _run("""
        MATCH (p:Person {infected: true})
        OPTIONAL MATCH (p)-[:MET]-(contact:Person)
        RETURN p.id AS id, p.name AS name, p.city AS city,
               p.country AS country, p.role AS role,
               p.age AS age, p.gender AS gender,
               p.deceased AS deceased, p.recovered AS recovered,
               COUNT(DISTINCT contact) AS total_contacts
        ORDER BY p.country, p.city
    """)


# ── At-risk contacts ─────────────────────────────────────────────────────────

def get_at_risk(degrees=2):
    return _run(f"""
        MATCH (infected:Person {{infected: true}})-[:MET*1..{degrees}]-(atRisk:Person)
        WHERE atRisk.infected = false AND atRisk.deceased = false
        WITH atRisk,
             COUNT(DISTINCT infected) AS exposure_count
        RETURN atRisk.id AS id, atRisk.name AS name, atRisk.city AS city,
               atRisk.country AS country, atRisk.role AS role,
               atRisk.age AS age, exposure_count,
               CASE WHEN exposure_count >= 3 THEN 'Critical'
                    WHEN exposure_count >= 2 THEN 'High'
                    ELSE 'Medium' END AS risk_level
        ORDER BY exposure_count DESC, atRisk.country
    """)


# ── Infection chain (shortest path) ─────────────────────────────────────────

def get_infection_chain(start_name, end_name):
    rows = _run("""
        MATCH path = shortestPath(
            (a:Person {name: $start})-[:MET*]-(b:Person {name: $end})
        )
        RETURN [n IN nodes(path) | {name: n.name, city: n.city, country: n.country, infected: n.infected}] AS chain,
               length(path) AS hops,
               [r IN relationships(path) | {date: r.date, location: r.location, risk: r.risk}] AS events
    """, start=start_name, end=end_name)
    return rows[0] if rows else {"chain": [], "hops": 0, "events": []}


# ── Spread by country ────────────────────────────────────────────────────────

def get_country_spread():
    return _run("""
        MATCH (p:Person)
        RETURN p.country AS country,
               COUNT(p) AS total_people,
               SUM(CASE WHEN p.infected  THEN 1 ELSE 0 END) AS infected,
               SUM(CASE WHEN p.deceased  THEN 1 ELSE 0 END) AS deceased,
               SUM(CASE WHEN p.recovered THEN 1 ELSE 0 END) AS recovered
        ORDER BY infected DESC
    """)


# ── Spread by city ───────────────────────────────────────────────────────────

def get_city_spread():
    return _run("""
        MATCH (p:Person)
        RETURN p.city AS city, p.country AS country,
               COUNT(p) AS total_people,
               SUM(CASE WHEN p.infected  THEN 1 ELSE 0 END) AS infected,
               SUM(CASE WHEN p.deceased  THEN 1 ELSE 0 END) AS deceased
        ORDER BY infected DESC
    """)


# ── Super spreaders (most contacts) ─────────────────────────────────────────

def get_super_spreaders():
    return _run("""
        MATCH (p:Person {infected: true})-[:MET]-(contact:Person)
        WITH p, COUNT(DISTINCT contact) AS contact_count
        WHERE contact_count >= 3
        RETURN p.id AS id, p.name AS name, p.city AS city,
               p.country AS country, p.role AS role,
               contact_count
        ORDER BY contact_count DESC
        LIMIT 10
    """)


# ── Timeline of contacts ─────────────────────────────────────────────────────

def get_timeline():
    return _run("""
        MATCH (a:Person)-[r:MET]->(b:Person)
        WHERE a.infected = true OR b.infected = true
        RETURN DISTINCT r.date AS date, r.location AS location,
               r.country AS country, r.risk AS risk,
               a.name AS person_a, a.infected AS a_infected,
               b.name AS person_b, b.infected AS b_infected
        ORDER BY r.date
    """)


# ── High-risk contact events ─────────────────────────────────────────────────

def get_high_risk_events():
    return _run("""
        MATCH (a:Person)-[r:MET {risk: 'High'}]-(b:Person)
        WHERE a.infected = true
        RETURN DISTINCT a.name AS infected_person, b.name AS exposed_person,
               b.city AS city, b.country AS country,
               r.date AS date, r.location AS location,
               b.infected AS also_infected
        ORDER BY r.date DESC
        LIMIT 20
    """)


# ── Full graph for visualisation ─────────────────────────────────────────────

def get_graph():
    nodes_raw = _run("""
        MATCH (p:Person)
        RETURN p.id AS id, p.name AS name, p.city AS city,
               p.country AS country, p.role AS role,
               p.infected AS infected, p.deceased AS deceased,
               p.recovered AS recovered, p.age AS age
    """)
    edges_raw = _run("""
        MATCH (a:Person)-[r:MET]->(b:Person)
        RETURN a.id AS source, b.id AS target,
               r.date AS date, r.location AS location, r.risk AS risk
    """)
    # Deduplicate edges (undirected)
    seen = set()
    edges = []
    for e in edges_raw:
        key = tuple(sorted([e["source"], e["target"]]) + [e["date"]])
        if key not in seen:
            seen.add(key)
            edges.append(e)
    return {"nodes": nodes_raw, "edges": edges}


# ── Search person ────────────────────────────────────────────────────────────

def search_person(name):
    return _run("""
        MATCH (p:Person)
        WHERE toLower(p.name) CONTAINS toLower($name)
        OPTIONAL MATCH (p)-[r:MET]-(contact:Person)
        RETURN p.id AS id, p.name AS name, p.city AS city,
               p.country AS country, p.role AS role,
               p.infected AS infected, p.deceased AS deceased,
               p.recovered AS recovered, p.age AS age, p.gender AS gender,
               COUNT(DISTINCT contact) AS total_contacts
    """, name=name)


# ── Mark infected / quarantined ──────────────────────────────────────────────

def mark_infected(person_id):
    _run("MATCH (p:Person {id: $id}) SET p.infected = true", id=person_id)
    return {"status": "marked_infected", "id": person_id}

def mark_quarantined(person_id):
    _run("MATCH (p:Person {id: $id}) SET p.quarantined = true", id=person_id)
    return {"status": "quarantined", "id": person_id}

def mark_recovered(person_id):
    _run("MATCH (p:Person {id: $id}) SET p.infected = false, p.recovered = true", id=person_id)
    return {"status": "recovered", "id": person_id}
