import json
import sqlite3
import pandas as pd

# Load data
with open('data/raw_incidents.json', 'r') as f:
    incidents = json.load(f)

# Create DataFrame
df = pd.DataFrame(incidents)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour

# Add severity ranking
severity_map = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
df['severity_rank'] = df['severity'].map(severity_map)

# Create database
conn = sqlite3.connect('data/incidents.db')
df.to_sql('incidents', conn, if_exists='replace', index=False)
conn.close()

print("✅ Created database with 100 incidents!")
