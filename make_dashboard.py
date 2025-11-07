import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
conn = sqlite3.connect('data/incidents.db')
df = pd.read_sql_query('SELECT * FROM incidents', conn)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = pd.to_datetime(df['date'])
conn.close()

# Create output folder
import os
os.makedirs('outputs', exist_ok=True)

# Chart 1: Severity Pie
severity_counts = df['severity'].value_counts()
colors = {'Critical': '#FF4444', 'High': '#FF8C00', 'Medium': '#FFD700', 'Low': '#90EE90'}
fig1 = go.Figure(data=[go.Pie(
    labels=severity_counts.index,
    values=severity_counts.values,
    hole=0.4,
    marker=dict(colors=[colors[s] for s in severity_counts.index])
)])
fig1.update_layout(title='<b>Severity Distribution</b>', height=500)
fig1.write_html('outputs/severity.html')

# Chart 2: Timeline
timeline = df.groupby('date').size().reset_index(name='count')
fig2 = px.line(timeline, x='date', y='count', title='<b>Incidents Over Time</b>')
fig2.write_html('outputs/timeline.html')

# Create main dashboard
total = len(df)
critical = len(df[df['severity']=='Critical'])
avg_response = df['response_time_hours'].mean()
total_cost = df['cost_impact'].sum()

html = f"""
<!DOCTYPE html>
<html>
<head><title>SecOps Dashboard</title>
<style>
body {{font-family: Arial; margin: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}}
.container {{max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px;}}
h1 {{text-align: center; color: #2C3E50;}}
.stats {{display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0;}}
.stat-card {{background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center;}}
.stat-value {{font-size: 32px; font-weight: bold;}}
.stat-label {{font-size: 12px; text-transform: uppercase;}}
iframe {{width: 100%; height: 500px; border: none; margin: 20px 0;}}
</style>
</head>
<body>
<div class="container">
<h1>🛡️ SecOps Insight Dashboard</h1>
<div class="stats">
<div class="stat-card"><div class="stat-label">Total Incidents</div><div class="stat-value">{total}</div></div>
<div class="stat-card"><div class="stat-label">Critical</div><div class="stat-value">{critical}</div></div>
<div class="stat-card"><div class="stat-label">Avg Response</div><div class="stat-value">{avg_response:.1f}h</div></div>
<div class="stat-card"><div class="stat-label">Cost Impact</div><div class="stat-value">${total_cost:,.0f}</div></div>
</div>
<iframe src="severity.html"></iframe>
<iframe src="timeline.html"></iframe>
</div>
</body>
</html>
"""

with open('outputs/dashboard.html', 'w') as f:
    f.write(html)

print("✅ Dashboard created!")
print("👉 Open: outputs/dashboard.html")
