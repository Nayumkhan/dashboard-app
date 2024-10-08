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
            dcc.Input(id=f'input-{category}', type='number', placeholder='Enter Value'),
            html.Button('Update', id=f'update-button-{category}', n_clicks=0)
        ]) for category in df['Category']
    ], style={'margin-bottom': '20px'}),
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input(f'update-button-{category}', 'n_clicks') for category in df['Category']],
    [Input(f'input-{category}', 'value') for category in df['Category']]
)
def update_chart(*args):
    global df
    for i, category in enumerate(df['Category']):
        n_clicks = args[i]
        new_value = args[len(df['Category']) + i]
        if n_clicks > 0 and new_value is not None:
            df.loc[df['Category'] == category, 'Values'] = new_value

    bar_fig = px.bar(df, x='Category', y='Values', title='Bar Chart of Truck Categories',
                     color='Category', 
                     color_discrete_map={
                         "Available Trucks": "green",
                         "Trucks in Operation": "blue",
                         "Waiting Load": "orange",
                         "Under Offload": "purple",
                         "Breakdown": "red"
                     })

    pie_fig = px.pie(df, values='Values', names='Category', title='Distribution of Truck Categories')

    return bar_fig, pie_fig

if __name__ == '__main__':
    app.run_server(debug=True)

application = app.server
