# 🦠 Ebola Contact Tracer
### Real-time outbreak surveillance · DRC · Uganda · Rwanda

A production-grade graph database application that models Ebola outbreak contact tracing across Central & East Africa. Built with **Neo4j AuraDB**, **Python/Flask**, and a live dashboard frontend.

---

## 🎯 What This Solves

During the 2018–2020 DRC Ebola outbreak, contact tracing was done **manually** — taking days or weeks to identify at-risk people. This system does it in **milliseconds** using graph traversal.

Given: *"Amani in Goma just tested positive"*
This system instantly answers:
- Who did Amani contact directly? (1st degree)
- Who did *those* people contact? (2nd degree)
- What is the exact transmission path from Goma to Kigali?
- Which cities/countries are at risk?
- Who are the super-spreaders?

---

## 🏗 Architecture

```
Neo4j AuraDB (Graph Database)
        ↕
Flask REST API (Python backend)
        ↕
HTML Dashboard (Frontend)
```

**Graph Model:**
```
(:Person {name, city, country, role, age, infected, ...})
    -[:MET {date, location, risk}]->
(:Person)

(:Person)-[:LIVES_IN]->(:Country)
```

---

## 📊 Dataset

| Metric | Count |
|---|---|
| People tracked | 60 |
| Contact events | 100+ |
| Countries | DRC, Uganda, Rwanda, Kenya |
| Cities | Goma, Butembo, Beni, Kampala, Kasese, Kigali, Rubavu, Musanze, Huye |
| Confirmed infected | 8 |
| Deceased | 3 |
| Recovered | 2 |

---

## 🚀 Setup (10 minutes)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ebola-contact-tracer.git
cd ebola-contact-tracer
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Neo4j credentials
Copy `.env.example` to `.env` and fill in your AuraDB details:
```bash
cp .env.example .env
```
```env
NEO4J_URI=neo4j+s://YOUR_INSTANCE.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=YOUR_PASSWORD
NEO4J_DATABASE=neo4j
```

### 5. Seed the database
```bash
cd backend
python seed_data.py
```

### 6. Start the API
```bash
python app.py
```

### 7. Open the dashboard
Open `frontend/index.html` in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/stats` | Dashboard summary stats |
| GET | `/infected` | All confirmed cases |
| GET | `/at-risk?degrees=2` | People at risk (1–3 degrees) |
| GET | `/chain?from=Name&to=Name` | Shortest infection path |
| GET | `/spread/country` | Cases per country |
| GET | `/spread/city` | Cases per city |
| GET | `/super-spreaders` | Most connected infected people |
| GET | `/timeline` | All contact events chronologically |
| GET | `/high-risk-events` | High-risk exposures |
| GET | `/graph` | Full graph for visualisation |
| GET | `/search?name=...` | Search by name |
| POST | `/mark/infected/:id` | Mark person as infected |
| POST | `/mark/quarantined/:id` | Mark as quarantined |
| POST | `/mark/recovered/:id` | Mark as recovered |

---

## 🧪 Demo Queries (Cypher)

Run these directly in Neo4j Browser (`https://console.neo4j.io`):

```cypher
// View entire network
MATCH (p:Person)-[r:MET]-(q:Person)
RETURN p, r, q LIMIT 100

// Who is infected?
MATCH (p:Person {infected: true})
RETURN p.name, p.city, p.country

// How did virus travel from Goma to Kigali?
MATCH path = shortestPath(
  (a:Person {name: "Amani Kabila"})-[:MET*]-(b:Person {name: "Hope Uwase"})
)
RETURN path

// Everyone within 2 contacts of an infected person
MATCH (i:Person {infected: true})-[:MET*1..2]-(atRisk:Person)
WHERE atRisk.infected = false
RETURN DISTINCT atRisk.name, atRisk.city, atRisk.country

// Super spreaders
MATCH (p:Person {infected: true})-[:MET]-(c:Person)
WITH p, COUNT(DISTINCT c) AS contacts
ORDER BY contacts DESC
RETURN p.name, p.city, contacts LIMIT 10
```

---

## 📸 Workshop Presentation Flow

1. **The Problem** — "Manual contact tracing during COVID/Ebola took weeks"
2. **The Graph Model** — Show nodes and relationships in Neo4j Browser
3. **Live Demo: Patient Zero** — Run `MATCH (p:Person {infected:true}) RETURN p`
4. **Trace the spread** — Run the shortest path query Goma → Kigali
5. **Dashboard** — Open `frontend/index.html` and click through
6. **Mark new case** — `POST /mark/infected/p05` and refresh dashboard
7. **The impact** — "This runs in 2ms. Manual tracing took 2 weeks."

---

## 🛠 Tech Stack

- **Neo4j AuraDB** — Graph database (free tier)
- **Python 3.10+** — Backend language
- **Flask** — REST API framework
- **python-dotenv** — Environment config
- **HTML/CSS/JS** — Frontend (no framework needed)

---

## 👨‍💻 Author

Built by **Samson Niyizurugero**

---

## 📄 License

MIT License — free to use, modify, and present.
