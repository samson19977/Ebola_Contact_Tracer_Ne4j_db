"""
Ebola Outbreak Contact Tracer - Seed Data
Realistic outbreak simulation: DRC → Uganda → Rwanda
60 people, 100+ contacts, multiple clusters
"""
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os, time

load_dotenv()

URI      = os.getenv("NEO4J_URI")
USER     = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# ── 60 people across 3 countries ────────────────────────────────────────────
PEOPLE = [
    # DRC – Goma cluster (Patient Zero origin)
    {"id":"p01","name":"Amani Kabila",      "city":"Goma",       "country":"DRC",    "role":"Farmer",          "age":34,"gender":"M"},
    {"id":"p02","name":"Bahati Mwamba",     "city":"Goma",       "country":"DRC",    "role":"Nurse",           "age":28,"gender":"F"},
    {"id":"p03","name":"Celestin Nkurunziza","city":"Goma",      "country":"DRC",    "role":"Doctor",          "age":42,"gender":"M"},
    {"id":"p04","name":"Dorcas Muteba",     "city":"Goma",       "country":"DRC",    "role":"Market Trader",   "age":31,"gender":"F"},
    {"id":"p05","name":"Edouard Kalinda",   "city":"Goma",       "country":"DRC",    "role":"Bus Driver",      "age":45,"gender":"M"},
    {"id":"p06","name":"Faida Lukeba",      "city":"Goma",       "country":"DRC",    "role":"Teacher",         "age":27,"gender":"F"},
    {"id":"p07","name":"Gloire Tshibanda",  "city":"Goma",       "country":"DRC",    "role":"Pastor",          "age":55,"gender":"M"},
    {"id":"p08","name":"Honorine Mbuyi",    "city":"Goma",       "country":"DRC",    "role":"Farmer",          "age":38,"gender":"F"},
    {"id":"p09","name":"Innocent Mulumba",  "city":"Goma",       "country":"DRC",    "role":"Police Officer",  "age":33,"gender":"M"},
    {"id":"p10","name":"Jolie Kasongo",     "city":"Goma",       "country":"DRC",    "role":"Student",         "age":21,"gender":"F"},

    # DRC – Butembo cluster
    {"id":"p11","name":"Kambale Vihamba",   "city":"Butembo",    "country":"DRC",    "role":"Miner",           "age":29,"gender":"M"},
    {"id":"p12","name":"Lucie Paluku",      "city":"Butembo",    "country":"DRC",    "role":"Nurse",           "age":36,"gender":"F"},
    {"id":"p13","name":"Mapendo Siviri",    "city":"Butembo",    "country":"DRC",    "role":"Market Trader",   "age":44,"gender":"F"},
    {"id":"p14","name":"Ndungo Kakule",     "city":"Butembo",    "country":"DRC",    "role":"Teacher",         "age":39,"gender":"M"},
    {"id":"p15","name":"Olivier Katembo",   "city":"Butembo",    "country":"DRC",    "role":"Pharmacist",      "age":47,"gender":"M"},

    # DRC – Beni cluster
    {"id":"p16","name":"Perpetue Masika",   "city":"Beni",       "country":"DRC",    "role":"Midwife",         "age":32,"gender":"F"},
    {"id":"p17","name":"Quentin Muhindo",   "city":"Beni",       "country":"DRC",    "role":"Farmer",          "age":41,"gender":"M"},
    {"id":"p18","name":"Rachel Kavira",     "city":"Beni",       "country":"DRC",    "role":"Health Worker",   "age":26,"gender":"F"},
    {"id":"p19","name":"Samuel Kighoma",    "city":"Beni",       "country":"DRC",    "role":"Driver",          "age":37,"gender":"M"},
    {"id":"p20","name":"Therese Vihamba",   "city":"Beni",       "country":"DRC",    "role":"Nurse",           "age":30,"gender":"F"},

    # Uganda – Kampala cluster
    {"id":"p21","name":"Achiro Grace",      "city":"Kampala",    "country":"Uganda", "role":"Trader",          "age":35,"gender":"F"},
    {"id":"p22","name":"Byaruhanga Moses",  "city":"Kampala",    "country":"Uganda", "role":"Taxi Driver",     "age":40,"gender":"M"},
    {"id":"p23","name":"Chelimo Fatuma",    "city":"Kampala",    "country":"Uganda", "role":"Nurse",           "age":29,"gender":"F"},
    {"id":"p24","name":"Draleru Patrick",   "city":"Kampala",    "country":"Uganda", "role":"Doctor",          "age":48,"gender":"M"},
    {"id":"p25","name":"Emiru Joseph",      "city":"Kampala",    "country":"Uganda", "role":"Pastor",          "age":52,"gender":"M"},
    {"id":"p26","name":"Fiona Auma",        "city":"Kampala",    "country":"Uganda", "role":"Teacher",         "age":33,"gender":"F"},
    {"id":"p27","name":"Geoffrey Okello",   "city":"Kampala",    "country":"Uganda", "role":"Student",         "age":22,"gender":"M"},
    {"id":"p28","name":"Helen Atim",        "city":"Kampala",    "country":"Uganda", "role":"Market Trader",   "age":44,"gender":"F"},

    # Uganda – Kasese cluster (near DRC border)
    {"id":"p29","name":"Isaac Muhwezi",     "city":"Kasese",     "country":"Uganda", "role":"Border Officer",  "age":36,"gender":"M"},
    {"id":"p30","name":"Joyce Kyakimwa",    "city":"Kasese",     "country":"Uganda", "role":"Farmer",          "age":31,"gender":"F"},
    {"id":"p31","name":"Kenneth Bwambale",  "city":"Kasese",     "country":"Uganda", "role":"Miner",           "age":27,"gender":"M"},
    {"id":"p32","name":"Lydia Muhindo",     "city":"Kasese",     "country":"Uganda", "role":"Health Worker",   "age":38,"gender":"F"},
    {"id":"p33","name":"Martin Baluku",     "city":"Kasese",     "country":"Uganda", "role":"Driver",          "age":43,"gender":"M"},

    # Uganda – Mbarara cluster
    {"id":"p34","name":"Nakato Sarah",      "city":"Mbarara",    "country":"Uganda", "role":"Nurse",           "age":30,"gender":"F"},
    {"id":"p35","name":"Ochieng David",     "city":"Mbarara",    "country":"Uganda", "role":"Teacher",         "age":37,"gender":"M"},
    {"id":"p36","name":"Patience Akello",   "city":"Mbarara",    "country":"Uganda", "role":"Farmer",          "age":25,"gender":"F"},

    # Rwanda – Kigali cluster
    {"id":"p37","name":"Amahoro Diane",     "city":"Kigali",     "country":"Rwanda", "role":"Nurse",           "age":28,"gender":"F"},
    {"id":"p38","name":"Bizimana Eric",     "city":"Kigali",     "country":"Rwanda", "role":"Doctor",          "age":45,"gender":"M"},
    {"id":"p39","name":"Cyusa Jean",        "city":"Kigali",     "country":"Rwanda", "role":"Teacher",         "age":34,"gender":"M"},
    {"id":"p40","name":"Dusengimana Alice", "city":"Kigali",     "country":"Rwanda", "role":"Student",         "age":20,"gender":"F"},
    {"id":"p41","name":"Emile Habimana",    "city":"Kigali",     "country":"Rwanda", "role":"Bus Driver",      "age":41,"gender":"M"},
    {"id":"p42","name":"Flavia Mukamana",   "city":"Kigali",     "country":"Rwanda", "role":"Market Trader",   "age":36,"gender":"F"},
    {"id":"p43","name":"Gaspard Niyonzima", "city":"Kigali",     "country":"Rwanda", "role":"Pastor",          "age":50,"gender":"M"},
    {"id":"p44","name":"Hope Uwase",        "city":"Kigali",     "country":"Rwanda", "role":"Pharmacist",      "age":32,"gender":"F"},

    # Rwanda – Rubavu cluster (near DRC border)
    {"id":"p45","name":"Innocent Nzabonimpa","city":"Rubavu",    "country":"Rwanda", "role":"Border Officer",  "age":38,"gender":"M"},
    {"id":"p46","name":"Josephine Kayitesi","city":"Rubavu",     "country":"Rwanda", "role":"Trader",          "age":33,"gender":"F"},
    {"id":"p47","name":"Kevin Hakizimana",  "city":"Rubavu",     "country":"Rwanda", "role":"Farmer",          "age":29,"gender":"M"},
    {"id":"p48","name":"Liliane Mukeshimana","city":"Rubavu",    "country":"Rwanda", "role":"Nurse",           "age":26,"gender":"F"},

    # Rwanda – Musanze cluster
    {"id":"p49","name":"Marc Ndayisaba",    "city":"Musanze",    "country":"Rwanda", "role":"Teacher",         "age":40,"gender":"M"},
    {"id":"p50","name":"Nadine Umurerwa",   "city":"Musanze",    "country":"Rwanda", "role":"Farmer",          "age":35,"gender":"F"},
    {"id":"p51","name":"Oscar Habimana",    "city":"Musanze",    "country":"Rwanda", "role":"Driver",          "age":31,"gender":"M"},
    {"id":"p52","name":"Pascaline Ingabire","city":"Musanze",    "country":"Rwanda", "role":"Health Worker",   "age":27,"gender":"F"},

    # Rwanda – Huye cluster
    {"id":"p53","name":"Quentin Nshimiyimana","city":"Huye",     "country":"Rwanda", "role":"Student",         "age":22,"gender":"M"},
    {"id":"p54","name":"Rose Mukamuganga",  "city":"Huye",       "country":"Rwanda", "role":"Nurse",           "age":29,"gender":"F"},
    {"id":"p55","name":"Simon Nkurunziza",  "city":"Huye",       "country":"Rwanda", "role":"Teacher",         "age":44,"gender":"M"},

    # International travellers (high-risk spreaders)
    {"id":"p56","name":"Tariq Al-Amin",     "city":"Nairobi",    "country":"Kenya",  "role":"Aid Worker",      "age":39,"gender":"M"},
    {"id":"p57","name":"Uwimana Claire",    "city":"Kigali",     "country":"Rwanda", "role":"Flight Attendant","age":31,"gender":"F"},
    {"id":"p58","name":"Valentin Mugabo",   "city":"Kigali",     "country":"Rwanda", "role":"Health Official", "age":48,"gender":"M"},
    {"id":"p59","name":"Winnie Namukasa",   "city":"Entebbe",    "country":"Uganda", "role":"Aid Worker",      "age":35,"gender":"F"},
    {"id":"p60","name":"Xavier Ndorimana",  "city":"Kigali",     "country":"Rwanda", "role":"Epidemiologist",  "age":42,"gender":"M"},
]

# ── Contact events ────────────────────────────────────────────────────────────
CONTACTS = [
    # DRC Goma internal spread
    ("p01","p02","2025-01-03","Goma General Hospital",  "DRC",   "High"),
    ("p01","p04","2025-01-04","Goma Central Market",    "DRC",   "Medium"),
    ("p01","p07","2025-01-05","Sunday Church Service",  "DRC",   "High"),
    ("p02","p03","2025-01-05","Goma Hospital Ward",     "DRC",   "High"),
    ("p02","p08","2025-01-06","Neighbourhood Meeting",  "DRC",   "Medium"),
    ("p03","p09","2025-01-06","Police Station Visit",   "DRC",   "Low"),
    ("p04","p05","2025-01-07","Goma Bus Terminal",      "DRC",   "Medium"),
    ("p04","p06","2025-01-07","Goma Market",            "DRC",   "High"),
    ("p05","p11","2025-01-08","Goma-Butembo Road",      "DRC",   "Medium"),
    ("p06","p10","2025-01-08","Goma Secondary School",  "DRC",   "High"),
    ("p07","p08","2025-01-09","Church Fellowship",      "DRC",   "High"),
    ("p08","p16","2025-01-10","Beni Maternity Clinic",  "DRC",   "High"),
    ("p09","p17","2025-01-10","Beni Market",            "DRC",   "Medium"),

    # DRC Butembo cluster
    ("p11","p12","2025-01-09","Butembo Health Centre",  "DRC",   "High"),
    ("p11","p13","2025-01-10","Butembo Market",         "DRC",   "Medium"),
    ("p12","p15","2025-01-11","Butembo Pharmacy",       "DRC",   "Medium"),
    ("p13","p14","2025-01-11","Butembo School",         "DRC",   "Low"),
    ("p14","p19","2025-01-12","Butembo-Beni Highway",   "DRC",   "Low"),
    ("p15","p18","2025-01-12","Butembo Clinic",         "DRC",   "High"),

    # DRC Beni cluster
    ("p16","p17","2025-01-11","Beni Hospital",          "DRC",   "High"),
    ("p16","p20","2025-01-12","Beni Maternity Ward",    "DRC",   "High"),
    ("p17","p19","2025-01-12","Beni Taxi Park",         "DRC",   "Medium"),
    ("p18","p20","2025-01-13","Beni Health Post",       "DRC",   "High"),
    ("p19","p33","2025-01-14","DRC-Uganda Border Road", "Border","High"),

    # DRC → Uganda border crossing
    ("p05","p29","2025-01-13","Kasindi Border Post",    "Border","High"),
    ("p11","p31","2025-01-14","Kasese Border Market",   "Border","Medium"),
    ("p13","p30","2025-01-14","Kasese Town Market",     "Uganda","Medium"),

    # Uganda Kasese cluster
    ("p29","p30","2025-01-14","Kasese Border Post",     "Uganda","High"),
    ("p29","p32","2025-01-15","Kasese Health Centre",   "Uganda","High"),
    ("p30","p31","2025-01-15","Kasese Market",          "Uganda","Medium"),
    ("p31","p33","2025-01-15","Kasese Mine Site",       "Uganda","Medium"),
    ("p32","p34","2025-01-16","Mbarara Referral Hospital","Uganda","High"),
    ("p33","p22","2025-01-16","Kampala-Kasese Highway", "Uganda","Medium"),

    # Uganda Kampala cluster
    ("p22","p21","2025-01-17","Kampala Taxi Park",      "Uganda","High"),
    ("p22","p25","2025-01-17","Kampala Church",         "Uganda","High"),
    ("p21","p23","2025-01-18","Kampala Market",         "Uganda","Medium"),
    ("p21","p28","2025-01-18","Owino Market Kampala",   "Uganda","High"),
    ("p23","p24","2025-01-18","Mulago Hospital",        "Uganda","High"),
    ("p24","p26","2025-01-19","Kampala School",         "Uganda","Low"),
    ("p25","p27","2025-01-19","Kampala Church Youth",   "Uganda","High"),
    ("p28","p36","2025-01-20","Mbarara Market",         "Uganda","Medium"),
    ("p34","p35","2025-01-20","Mbarara Hospital",       "Uganda","High"),
    ("p35","p36","2025-01-21","Mbarara School",         "Uganda","Low"),

    # Uganda → Rwanda border crossing
    ("p22","p41","2025-01-20","Katuna Border Post",     "Border","High"),
    ("p21","p46","2025-01-20","Cyanika Border",         "Border","Medium"),
    ("p33","p45","2025-01-21","Rusizi Border Post",     "Border","High"),
    ("p59","p57","2025-01-21","Entebbe Airport",        "Uganda","Medium"),

    # Rwanda Rubavu cluster (near Goma border)
    ("p45","p46","2025-01-21","Rubavu Border Post",     "Rwanda","High"),
    ("p45","p47","2025-01-22","Rubavu Market",          "Rwanda","Medium"),
    ("p46","p48","2025-01-22","Rubavu Health Centre",   "Rwanda","High"),
    ("p47","p49","2025-01-23","Rubavu-Musanze Road",    "Rwanda","Low"),

    # Rwanda Musanze cluster
    ("p49","p50","2025-01-23","Musanze Market",         "Rwanda","Medium"),
    ("p50","p51","2025-01-24","Musanze Bus Park",       "Rwanda","Medium"),
    ("p51","p41","2025-01-24","Musanze-Kigali Highway", "Rwanda","High"),
    ("p52","p48","2025-01-24","Musanze Health Post",    "Rwanda","High"),

    # Rwanda Kigali cluster
    ("p41","p37","2025-01-25","Kigali Bus Station",     "Rwanda","High"),
    ("p41","p42","2025-01-25","Nyabugogo Market",       "Rwanda","High"),
    ("p37","p38","2025-01-25","CHUK Hospital Kigali",   "Rwanda","High"),
    ("p37","p44","2025-01-26","Kigali Pharmacy",        "Rwanda","Medium"),
    ("p38","p58","2025-01-26","Ministry of Health",     "Rwanda","Medium"),
    ("p38","p60","2025-01-26","CHUK Hospital Meeting",  "Rwanda","Low"),
    ("p39","p40","2025-01-26","Kigali Secondary School","Rwanda","High"),
    ("p42","p43","2025-01-27","Kigali Church",          "Rwanda","High"),
    ("p43","p53","2025-01-27","Kigali-Huye Bus",        "Rwanda","Medium"),
    ("p44","p57","2025-01-27","Kigali Airport",         "Rwanda","Low"),
    ("p57","p59","2025-01-28","Kigali Airport Lounge",  "Rwanda","Medium"),
    ("p58","p60","2025-01-28","RBC Headquarters",       "Rwanda","Low"),

    # Rwanda Huye cluster
    ("p53","p54","2025-01-28","Huye Market",            "Rwanda","Medium"),
    ("p54","p55","2025-01-28","Huye Health Centre",     "Rwanda","High"),
    ("p55","p50","2025-01-29","Huye-Musanze Route",     "Rwanda","Low"),

    # International aid worker connections
    ("p56","p03","2025-01-07","WHO Emergency Meeting",  "DRC",   "Low"),
    ("p56","p38","2025-01-26","WHO Kigali Office",      "Rwanda","Low"),
    ("p59","p32","2025-01-16","MSF Kasese Base",        "Uganda","Medium"),
    ("p60","p24","2025-01-23","Epidemiology Conference","Uganda","Low"),
]

# ── First 8 people confirmed infected (Patient Zero = p01) ──────────────────
INFECTED = ["p01", "p02", "p04", "p07", "p11", "p16", "p29", "p45"]

# ── Deceased ─────────────────────────────────────────────────────────────────
DECEASED = ["p01", "p07", "p16"]

# ── Recovered ────────────────────────────────────────────────────────────────
RECOVERED = ["p02", "p11"]

def seed():
    print("🔗 Connecting to Neo4j AuraDB...")
    with driver.session(database=DATABASE) as session:
        print("🧹 Clearing existing data...")
        session.run("MATCH (n) DETACH DELETE n")

        print(f"👤 Creating {len(PEOPLE)} people...")
        for p in PEOPLE:
            session.run("""
                CREATE (person:Person {
                    id: $id, name: $name, city: $city,
                    country: $country, role: $role,
                    age: $age, gender: $gender,
                    infected: false, deceased: false, recovered: false,
                    quarantined: false
                })
            """, **p)

        print(f"🤝 Creating {len(CONTACTS)} contact events...")
        for a, b, date, location, country, risk in CONTACTS:
            session.run("""
                MATCH (pa:Person {id: $a}), (pb:Person {id: $b})
                CREATE (pa)-[:MET {date: $date, location: $location, country: $country, risk: $risk}]->(pb)
                CREATE (pb)-[:MET {date: $date, location: $location, country: $country, risk: $risk}]->(pa)
            """, a=a, b=b, date=date, location=location, country=country, risk=risk)

        print("🦠 Marking infected cases...")
        for pid in INFECTED:
            session.run("MATCH (p:Person {id: $id}) SET p.infected = true", id=pid)

        print("💀 Marking deceased...")
        for pid in DECEASED:
            session.run("MATCH (p:Person {id: $id}) SET p.deceased = true", id=pid)

        print("💚 Marking recovered...")
        for pid in RECOVERED:
            session.run("MATCH (p:Person {id: $id}) SET p.infected = false, p.recovered = true", id=pid)

        # Create country nodes
        print("🌍 Creating country summary nodes...")
        for country in ["DRC", "Uganda", "Rwanda", "Kenya"]:
            session.run("MERGE (:Country {name: $name})", name=country)
        for p in PEOPLE:
            session.run("""
                MATCH (person:Person {id: $id}), (c:Country {name: $country})
                MERGE (person)-[:LIVES_IN]->(c)
            """, id=p["id"], country=p["country"])

    print("\n✅ DATABASE SEEDED SUCCESSFULLY!")
    print(f"   👥 {len(PEOPLE)} people across DRC, Uganda, Rwanda, Kenya")
    print(f"   🤝 {len(CONTACTS)} contact events")
    print(f"   🦠 {len(INFECTED)} confirmed infections")
    print(f"   💀 {len(DECEASED)} deceased")
    print(f"   💚 {len(RECOVERED)} recovered")
    driver.close()

if __name__ == "__main__":
    seed()
