import json
import os
from datetime import datetime, timedelta
import random

# Create data folder
os.makedirs('data', exist_ok=True)

# Generate sample incidents
incidents = []
incident_types = ['Malware', 'Phishing', 'DDoS', 'Data Breach', 'Ransomware', 
                  'Unauthorized Access', 'SQL Injection', 'Brute Force', 
                  'Insider Threat', 'Zero-Day Exploit']
severities = ['Critical', 'High', 'Medium', 'Low']
statuses = ['Open', 'In Progress', 'Resolved', 'Closed']

random.seed(42)
for i in range(100):
    days_ago = random.randint(0, 30)
    hours_ago = random.randint(0, 23)
    incident_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
    
    incidents.append({
        'incident_id': f'INC-2024-{1000 + i}',
        'type': random.choice(incident_types),
        'severity': random.choice(severities),
        'status': random.choice(statuses),
        'timestamp': incident_time.strftime('%Y-%m-%d %H:%M:%S'),
        'affected_systems': random.randint(1, 50),
        'response_time_hours': round(random.uniform(0.5, 48), 2),
        'cost_impact': random.randint(1000, 100000),
    })

# Save to file
with open('data/raw_incidents.json', 'w') as f:
    json.dump(incidents, f, indent=2)

print("✅ Created 100 sample incidents!")
