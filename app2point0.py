import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.DataFrame({
    "Category": ["Available Trucks", "Trucks in Operation", "Waiting Load", "Under Offload", "Breakdown"],
    "Values": [0, 0, 0, 0, 0]
})

app.layout = html.Div([
    html.H1("Truck Management Dashboard"),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
    
    html.Div([
        html.Div([
            html.Label(category),
            dcc.Input(id=f'input-{category}', type='number', placeholder='Add Value', min=0),
            html.Button('Add', id=f'add-button-{category}', n_clicks=0),
            html.Div(id=f'current-value-{category}', style={'margin-left': '10px'})
        ]) for category in df['Category']
    ], style={'margin-bottom': '20px'}),
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')] +
    [Output(f'current-value-{category}', 'children') for category in df['Category']],
    [Input(f'add-button-{category}', 'n_clicks') for category in df['Category']],
    [Input(f'input-{category}', 'value') for category in df['Category']]
)
def update_chart(*args):
    global df

    total_trucks = df['Values'].sum()
    outputs = []

    for i, category in enumerate(df['Category']):
        n_clicks = args[i]
        new_value = args[len(df['Category']) + i]

        if n_clicks > 0 and new_value is not None:
            if total_trucks + new_value <= 20:
                df.loc[df['Category'] == category, 'Values'] += new_value
                total_trucks += new_value
            else:
                outputs.append(f'Cannot add {new_value}. Total trucks cannot exceed 20.')
                continue

        outputs.append(f'Current Value: {df.loc[df["Category"] == category, "Values"].values[0]}')

    bar_fig = px.bar(df, x='Category', y='Values', title='Bar Chart of Truck Categories')
    pie_fig = px.pie(df, values='Values', names='Category', title='Distribution of Truck Categories')

    return bar_fig, pie_fig, *outputs

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)

application = app.server
