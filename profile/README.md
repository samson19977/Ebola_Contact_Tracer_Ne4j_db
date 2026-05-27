# Ebola Contact Tracer – Project Profile

**Author:** Francis Musoke  
**Version:** 2.0.0  
**Region:** DRC · Uganda · Rwanda · Kenya

---

## Overview

A graph-database-powered contact tracing API for Ebola outbreak simulation across East & Central Africa. Built with Python/Flask and Neo4j AuraDB.

## Data Summary

| Category       | Count |
|---------------|-------|
| People tracked | 60    |
| Contact events | 100+  |
| Countries      | 4     |
| Infected       | 8     |
| Deceased       | 3     |
| Recovered      | 2     |

## Setup

### 1. Configure environment
Edit `.env` with your Neo4j AuraDB credentials:
```
NEO4J_URI=neo4j+s://<your-instance>.databases.neo4j.io
NEO4J_USERNAME=<username>
NEO4J_PASSWORD=<password>
NEO4J_DATABASE=<database>
```
> ⚠️ No trailing spaces after values — this causes the URI scheme error.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed the database
```bash
python seed_data.py
```

### 4. Run the API
```bash
python app.py
```

API runs at: http://localhost:5000

## Key API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/stats` | Dashboard totals (infected, deceased, at-risk, etc.) |
| `/infected` | All confirmed infected persons |
| `/at-risk` | Contacts at risk (1–2 degrees) |
| `/chain?from=X&to=Y` | Shortest infection path between two people |
| `/spread/country` | Spread breakdown by country |
| `/super-spreaders` | People with 3+ contacts |
| `/graph` | Full node/edge graph for visualisation |

## Common Error

**`URI scheme b'' is not supported`**  
**Cause:** Trailing spaces or Windows CRLF (`\r`) in `.env` file  
**Fix:** Remove all trailing whitespace from `.env` values
