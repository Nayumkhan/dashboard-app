import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

total_trucks = 0
df = pd.DataFrame({
    "Category": ["Available Trucks", "Trucks in Operation", "Waiting Load", "Under Offload", "Breakdown"],
    "Values": [0, 0, 0, 0, 0]
})

app.layout = html.Div([
    html.H1("Truck Management Dashboard"),
    html.Div([
        html.Label("Total number of Trucks"),
        dcc.Input(id='input-total-trucks', type='number', placeholder='Enter Total Trucks', value=''),
        html.Button('Update', id='update-button-total', n_clicks=0)
    ]),
    dcc.Graph(id='bar-chart', style={'height': '40vh'}),
    dcc.Graph(id='pie-chart', style={'height': '40vh'}),
    html.Div([
        html.Div([
            html.Label(category),
            dcc.Input(id=f'input-{category.replace(" ", "_")}', type='number', placeholder='Enter Value', value=''),
            html.Button('Update', id=f'update-button-{category.replace(" ", "_")}', n_clicks=0)
        ]) for category in df['Category']
    ], style={'margin-bottom': '20px'}),
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('input-total-trucks', 'value'),
     *[Output(f'input-{category.replace(" ", "_")}', 'value') for category in df['Category']]
    ],
    [Input('update-button-total', 'n_clicks')] + 
    [Input(f'update-button-{category.replace(" ", "_")}', 'n_clicks') for category in df['Category']] +
    [Input('input-total-trucks', 'value')] +
    [Input(f'input-{category.replace(" ", "_")}', 'value') for category in df['Category']]
)
def update_chart(*args):
    global total_trucks
    ctx = dash.callback_context

    if ctx.triggered:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Update total trucks
        if triggered_id == 'update-button-total':
            new_total = args[0]
            if new_total is not None and new_total != '':
                total_trucks = int(new_total)
                # Reset all category values
                df['Values'] = 0
                return create_figures(), '', '', *([''] * len(df['Category']))

        # Update category values
        for i, category in enumerate(df['Category']):
            if triggered_id == f'update-button-{category.replace(" ", "_")}':
                new_value = args[len(df['Category']) + 2 + i]
                if new_value is not None and new_value != '':
                    value_to_add = int(new_value)
                    if total_trucks >= value_to_add:
                        total_trucks -= value_to_add
                        df.loc[df['Category'] == category, 'Values'] += value_to_add

    # Return updated figures and empty inputs
    return create_figures(), '', '', *([''] * len(df['Category']))

def create_figures():
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
