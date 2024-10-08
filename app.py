import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

total_trucks = 0  # Set the initial total number of trucks to 0

df = pd.DataFrame({
    "Category": ["Available Trucks", "Trucks in Operation", "Waiting Load", "Under Offload", "Breakdown"],
    "Values": [0, 0, 0, 0, 0]
})

app.layout = html.Div([
    html.H1("Truck Management Dashboard"),
    html.Div([
        html.Label("Total Number of Trucks"),
        dcc.Input(id='input-total-trucks', type='number', placeholder='Enter Total Trucks'),
        html.Button('Update', id='update-button-total', n_clicks=0)
    ]),
    dcc.Graph(id='bar-chart', style={'height': '40vh'}),
    dcc.Graph(id='pie-chart', style={'height': '40vh'}),
    html.Div([
        html.Div([
            html.Label(category),
            dcc.Input(id=f'input-{category}', type='number', placeholder='Enter Value'),
            html.Button('Update', id=f'update-button-{category}', n_clicks=0)
        ], style={'margin-bottom': '10px'}) for category in df['Category']
    ], style={'margin-bottom': '20px'}),
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('input-total-trucks', 'value')] + 
     [Output(f'input-{category}', 'value') for category in df['Category']],
    [Input('update-button-total', 'n_clicks')] +
    [Input(f'update-button-{category}', 'n_clicks') for category in df['Category']],
    [Input('input-total-trucks', 'value')] + 
    [Input(f'input-{category}', 'value') for category in df['Category']]
)
def update_chart(*args):
    global total_trucks, df

    total_clicks = args[0]
    category_clicks = args[1:len(df['Category']) + 1]
    total_value = args[len(df['Category']) + 1]
    category_values = args[len(df['Category']) + 2:]

    if total_clicks > 0 and total_value is not None:
        total_trucks = total_value

    for i, category in enumerate(df['Category']):
        n_clicks = category_clicks[i]
        new_value = category_values[i]
        if n_clicks > 0 and new_value is not None:
            if total_trucks >= new_value:  # Only allow input if it does not exceed the total trucks
                total_trucks -= new_value
                df.loc[df['Category'] == category, 'Values'] += new_value

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

    return bar_fig, pie_fig, '' + '' + '' + '' + ''  # Clear the inputs by returning empty strings

if __name__ == '__main__':
    app.run_server(debug=True)
