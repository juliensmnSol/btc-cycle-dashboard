import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dash import Dash, html, dcc
import plotly.graph_objects as go
from scoring import calculate_score, get_indicator
import json

app = Dash(__name__)

def get_color(score):
    if score < 25:
        return "#00ff88"
    elif score < 45:
        return "#88ff00"
    elif score < 65:
        return "#ffdd00"
    elif score < 80:
        return "#ff8800"
    else:
        return "#ff2200"

def build_layout():
    # Récupère le score et les données
    score = calculate_score()
    
    if score is None:
        score = 0
    
    color = get_color(score)
    
    # Charge les prix BTC
    with open("data/btc_price.json", "r") as f:
        price_data = json.load(f)
    
    dates = [entry[0] for entry in price_data['prices']]
    prices = [entry[1] for entry in price_data['prices']]
    
    # Convertit timestamps en dates lisibles
    import datetime
    dates = [datetime.datetime.fromtimestamp(d/1000).strftime('%Y-%m-%d') for d in dates]
    
    # Graphique prix BTC
    price_chart = go.Figure()
    price_chart.add_trace(go.Scatter(
        x=dates, y=prices,
        fill='tozeroy',
        line=dict(color='#f7931a', width=2),
        fillcolor='rgba(247, 147, 26, 0.1)'
    ))
    price_chart.update_layout(
        title='Prix BTC — 365 jours',
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#1a1a2e',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#333'),
        yaxis=dict(gridcolor='#333')
    )
    
    # Jauge du score
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Score Cycle BTC", 'font': {'color': 'white', 'size': 20}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'white'},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 25], 'color': '#003300'},
                {'range': [25, 45], 'color': '#1a3300'},
                {'range': [45, 65], 'color': '#333300'},
                {'range': [65, 80], 'color': '#332200'},
                {'range': [80, 100], 'color': '#330000'},
            ],
        },
        number={'font': {'color': color, 'size': 48}}
    ))
    gauge.update_layout(
        paper_bgcolor='#1a1a2e',
        font=dict(color='white')
    )
    
    return html.Div([
        # Header
        html.Div([
            html.H1("BTC Cycle Bottom Detector",
                style={'color': '#f7931a', 'textAlign': 'center', 'marginBottom': '5px'}),
            html.P("Détection des bottoms de cycle BTC pour timing d'entrée sur SOL/ETH",
                style={'color': '#888', 'textAlign': 'center'})
        ], style={'padding': '20px', 'borderBottom': '1px solid #333'}),
        
        # Jauge centrale
        html.Div([
            dcc.Graph(figure=gauge, style={'height': '350px'})
        ]),
        
        # Indicateurs
        html.Div([
            html.Div([
                html.H3("NUPL", style={'color': '#888', 'margin': '0'}),
                html.H2(f"{round(get_indicator('https://bitcoin-data.com/v1/nupl', 'nupl') or 0, 3)}",
                    style={'color': 'white', 'margin': '5px 0'})
            ], style={'background': '#16213e', 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'flex': '1', 'margin': '5px'}),
            
            html.Div([
                html.H3("MVRV Z-Score", style={'color': '#888', 'margin': '0'}),
                html.H2(f"{round(get_indicator('https://bitcoin-data.com/v1/mvrv-zscore', 'mvrvZscore') or 0, 3)}",
                    style={'color': 'white', 'margin': '5px 0'})
            ], style={'background': '#16213e', 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'flex': '1', 'margin': '5px'}),
            
            html.Div([
                html.H3("Puell Multiple", style={'color': '#888', 'margin': '0'}),
                html.H2(f"{round(get_indicator('https://bitcoin-data.com/v1/puell-multiple', 'puellMultiple') or 0, 3)}",
                    style={'color': 'white', 'margin': '5px 0'})
            ], style={'background': '#16213e', 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'flex': '1', 'margin': '5px'}),
            
            html.Div([
                html.H3("RSI 1W", style={'color': '#888', 'margin': '0'}),
                html.H2("33.23", style={'color': 'white', 'margin': '5px 0'})
            ], style={'background': '#16213e', 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'flex': '1', 'margin': '5px'}),
            
        ], style={'display': 'flex', 'padding': '20px', 'gap': '10px'}),
        
        # Graphique prix
        html.Div([
            dcc.Graph(figure=price_chart)
        ], style={'padding': '0 20px 20px 20px'})
        
    ], style={'background': '#1a1a2e', 'minHeight': '100vh', 'fontFamily': 'Arial'})

app.layout = build_layout()

if __name__ == '__main__':
    print("Dashboard lancé sur http://localhost:8050")
    app.run(debug=False)