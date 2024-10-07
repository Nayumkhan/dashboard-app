<<<<<<< HEAD
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.DataFrame({
    "Category": ["Available Trucks", "Trucks in Operation", "Waiting Load", "Under Offload", "Breakdown"],
    "Values": [50, 30, 10, 5, 5]
})

app.layout = html.Div([
    html.H1("Truck Management Dashboard"),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
    
    html.Div([
        html.Div([
            html.Label(category),
            dcc.Input(id=f'input-{category}', type='number', placeholder='Add Value'),
            html.Button('Add', id=f'add-button-{category}', n_clicks=0)
        ]) for category in df['Category']
    ], style={'margin-bottom': '20px'}),
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input(f'add-button-{category}', 'n_clicks') for category in df['Category']],
    [Input(f'input-{category}', 'value') for category in df['Category']]
)
def update_chart(*args):
    global df

    for i, category in enumerate(df['Category']):
        n_clicks = args[i]
        new_value = args[len(df['Category']) + i]
        if n_clicks > 0 and new_value is not None:
            df.loc[df['Category'] == category, 'Values'] += new_value

    bar_fig = px.bar(df, x='Category', y='Values', title='Bar Chart of Truck Categories')
    pie_fig = px.pie(df, values='Values', names='Category', title='Distribution of Truck Categories')

    return bar_fig, pie_fig

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))  # Use the port assigned by Render, or default to 8050
    app.run_server(debug=False, host='0.0.0.0', port=port)
=======
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.DataFrame({
    "Category": ["Available Trucks", "Trucks in Operation", "Waiting Load", "Under Offload", "Breakdown"],
    "Values": [50, 30, 10, 5, 5]
})

app.layout = html.Div([
    html.H1("Truck Management Dashboard"),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
    
    html.Div([
        html.Div([
            html.Label(category),
            dcc.Input(id=f'input-{category}', type='number', placeholder='Add Value'),
            html.Button('Add', id=f'add-button-{category}', n_clicks=0)
        ]) for category in df['Category']
    ], style={'margin-bottom': '20px'}),
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input(f'add-button-{category}', 'n_clicks') for category in df['Category']],
    [Input(f'input-{category}', 'value') for category in df['Category']]
)
def update_chart(*args):
    global df

    for i, category in enumerate(df['Category']):
        n_clicks = args[i]
        new_value = args[len(df['Category']) + i]
        if n_clicks > 0 and new_value is not None:
            df.loc[df['Category'] == category, 'Values'] += new_value

    bar_fig = px.bar(df, x='Category', y='Values', title='Bar Chart of Truck Categories')
    pie_fig = px.pie(df, values='Values', names='Category', title='Distribution of Truck Categories')

    return bar_fig, pie_fig

if __name__ == '__main__':
    app.run_server(debug=True)

application = app.server


