import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

total_trucks = 20
balance = 20

df = pd.DataFrame({
    "Category": ["Available Trucks", "Waiting Load", "Under Offload", "Breakdown"],
    "Values": [0, 0, 0, 0]
})

app.layout = html.Div([
    html.H1("Truck Management Dashboard", style={'textAlign': 'center', 'fontSize': '36px'}),
    html.Div([
        html.Div(id='total-trucks-text', style={'fontSize': '22px', 'margin-right': '10px'}),
        html.Div(id='balance-text', style={'fontSize': '22px', 'margin-left': '10px'})
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),
    
    dcc.Graph(id='bar-chart', style={'display': 'inline-block', 'width': '48%', 'height': '400px'}),
    dcc.Graph(id='pie-chart', style={'display': 'inline-block', 'width': '48%', 'height': '400px'}),
    
    html.Div([
        html.Div([
            html.Label(category, style={'fontSize': '24px'}),
            dcc.Input(id=f'input-{category}', type='number', placeholder='Enter Value', style={'width': '150px'}),
            html.Button('Update', id=f'update-button-{category}', n_clicks=0, style={'margin-left': '5px'})
        ], style={'margin-bottom': '20px'}) for category in df['Category']
    ]),
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('balance-text', 'children')],
    [Input(f'update-button-{category}', 'n_clicks') for category in df['Category']] +
    [Input(f'input-{category}', 'value') for category in df['Category']]
)
def update_chart(*args):
    global df, balance
    trucks_accounted_for = 0

    for i, category in enumerate(df['Category']):
        n_clicks = args[i]
        new_value = args[len(df['Category']) + i]
        if n_clicks > 0 and new_value is not None:
            df.loc[df['Category'] == category, 'Values'] = new_value
            trucks_accounted_for += new_value

    remaining_trucks = balance - trucks_accounted_for
    total_text = f"Total Number of Trucks: {balance}"
    balance_text = f"Balance: {remaining_trucks}"

    bar_fig = px.bar(df, x='Category', y='Values', title='Bar Chart of Truck Categories',
                     color='Category', 
                     color_discrete_map={
                         "Available Trucks": "green",
                         "Waiting Load": "orange",
                         "Under Offload": "purple",
                         "Breakdown": "red"
                     })

    pie_fig = px.pie(df, values='Values', names='Category', title='Distribution of Truck Categories')

    return bar_fig, pie_fig, balance_text

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)