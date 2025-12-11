import pandas as pd
import plotly.express as px
import xlwings as xw
import os

# Charger les données
df = pd.read_excel("coordonnees_normalisees2.xlsx", sheet_name="Sheet1")
df = df[['Nom', 'Ville', 'longitude', 'latitude']]
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df = df.dropna(subset=['latitude', 'longitude'])

# Créer la carte interactive
fig = px.scatter_map(df, lat='latitude', lon='longitude', hover_name='Nom', hover_data=['Ville'], zoom=5, height=600)
fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})

# Exporter en HTML
html_file = "map_interactive.html"
fig.write_html(html_file, include_plotlyjs='cdn')

# Ouvrir Excel et mettre un lien cliquable vers le HTML
app = xw.App(visible=True)
wb = app.books.add()
ws = wb.sheets[0]
ws.range("A1").value = "Clique ici pour ouvrir la map interactive"
ws.range("A1").hyperlink = os.path.abspath(html_file)

print("Carte interactive prête : clique sur le lien dans Excel pour l’ouvrir.")
