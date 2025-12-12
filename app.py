from dash import Dash, dcc, html
import plotly.graph_objects as go

app = Dash()

# --- Colors for app ---
colors = {
    'background': '#212f45',
    'text': '#7FDBFF'
}

# ================================
# 1) HEIGHT BAR CHART
# ================================
categories = ["Männer", "Frauen", "Gesamt"]
heights = [1.79, 1.66, 1.73]   # in meters
colors_custom = ["#cb1dcd", "#b3fa9d", "blue"]

fig_height = go.Figure(
    data=[
        go.Bar(
            x=categories,
            y=heights,
            marker=dict(color=colors_custom)
        )
    ]
)

fig_height.update_layout(
    title="Durchschnittliche Körpergröße in Deutschland",
    xaxis_title="Kategorie",
    yaxis_title="Körpergröße (Meter)",
    yaxis=dict(range=[0, 2]),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# ================================
# 2) DUMBBELL PLOT - LIFE MILESTONES
# ================================
milestones = [
    "Erster Studienabschluss (Jahre)",
    "Studienzeit (Semester)",
    "Auszug aus Elternhaus (Jahre)",
    "Geburt erstes Kind (Jahre)",
    "Erste Eheschließung (Jahre)",
    "Renteneintrittsalter (Jahre)",
    "Versicherungsjahre bis Rente"
]

women_values = [23.4, 7.9, 23.1, 30.4, 32.9, 64.7, 37.7]
men_values = [23.9, 8.6, 24.6, 33.3, 35.3, 64.7, 41.4]

fig_dumbbell = go.Figure()

# Add lines connecting the dumbbells
for i, milestone in enumerate(milestones):
    fig_dumbbell.add_trace(go.Scatter(
        x=[women_values[i], men_values[i]],
        y=[milestone, milestone],
        mode='lines',
        line=dict(color='gray', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add dots for women
fig_dumbbell.add_trace(go.Scatter(
    x=women_values,
    y=milestones,
    mode='markers',
    name='Frauen',
    marker=dict(color='#b3fa9d', size=12, line=dict(color='white', width=2)),
    hovertemplate='<b>Frauen</b><br>%{y}<br>%{x}<extra></extra>'
))

# Add dots for men
fig_dumbbell.add_trace(go.Scatter(
    x=men_values,
    y=milestones,
    mode='markers',
    name='Männer',
    marker=dict(color='#cb1dcd', size=12, line=dict(color='white', width=2)),
    hovertemplate='<b>Männer</b><br>%{y}<br>%{x}<extra></extra>'
))

fig_dumbbell.update_layout(
    title="Lebensphasen: Frauen vs. Männer",
    xaxis_title="Alter/Dauer",
    yaxis=dict(autorange="reversed"),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# ================================
# 3) DAILY TIME USE BAR CHART
# ================================
time_categories = [
    'Unbezahlte Arbeit',
    'Erwerbstätigkeit & Bildung',
    'Freizeit',
    'Schlafen & Körperpflege'
]

# Convert hours and minutes to decimal hours for easier plotting
women_time = [3 + 56/60, 2 + 39/60, 5 + 55/60, 9 + 43/60]
men_time = [2 + 46/60, 3 + 40/60, 6 + 23/60, 9 + 28/60]

fig_time = go.Figure()

fig_time.add_trace(go.Bar(
    name='Frauen',
    x=time_categories,
    y=women_time,
    marker=dict(color='#b3fa9d')
))

fig_time.add_trace(go.Bar(
    name='Männer',
    x=time_categories,
    y=men_time,
    marker=dict(color='#cb1dcd')
))

fig_time.update_layout(
    title='Durchschnittstag: Zeitverwendung (Stunden)',
    xaxis_title='Aktivität',
    yaxis_title='Stunden pro Tag',
    barmode='group',
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# ================================
# 4) BODY WEIGHT BULLET CHART
# ================================
weight_female = 69.2
weight_male = 85.8
weight_total = 77.7

fig_bullet = go.Figure()

fig_bullet.add_trace(go.Indicator(
    mode="number+gauge",
    value=weight_total,
    number={'suffix': " kg", 'font': {'size': 20}},   # smaller text
    title={'text': "Body Weight", 'font': {'size': 18}},  # smaller title
    gauge={
        'shape': "bullet",
        'axis': {'range': [0, 90]},
        'bar': {'color': "blue", 'thickness': 0.25},  # <-- thinner bar
        'steps': [
            {'range': [0, weight_female], 'color': "#b3fa9d"},
            {'range': [weight_female, weight_male], 'color': "#cb1dcd"}
        ]
    }
))

fig_bullet.update_layout(
    height=120,                     # <-- MUCH smaller chart height
    margin=dict(l=150, r=40, t=40, b=10), # moved to left to display lettering
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    font_color=colors['text']
)

# ================================
# DASH LAYOUT
# ================================
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(
        children='Der Durchschnittsmensch in Deutschland',
        style={'textAlign': 'center', 'color': colors['text']}
    ),

    html.Div(children='''
        Wie alt ist und wird er, wie sehen seine Lebensphasen aus?
        Wie lebt und wohnt er? Wie arbeitet der Durchschnittsmensch
        und wie verbringt er seine Zeit? Und wie viel Geld verdient
        er oder hat er zur Verfügung?
    ''',
    style={'textAlign': 'center', 'color': colors['text']}
    ),

    # --- HEIGHT BAR CHART AND DUMBBELL PLOT SIDE BY SIDE ---
    html.Div([
        html.Div([
            dcc.Graph(id='height-chart', figure=fig_height),
            # --- BODY WEIGHT BULLET CHART ---
            dcc.Graph(id='weight-bullet', figure=fig_bullet)
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        html.Div([
            dcc.Graph(id='dumbbell-plot', figure=fig_dumbbell)
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),
    
    # --- DAILY TIME USE BAR CHART (below dumbbell, next to bullet) ---
    html.Div([
        html.Div(style={'width': '48%', 'display': 'inline-block'}),  # empty space to align
        
        html.Div([
            dcc.Graph(id='time-chart', figure=fig_time)
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),
    
])

if __name__ == '__main__':
    app.run(debug=True)