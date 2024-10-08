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
    dcc.Tabs([
        dcc.Tab(label='Truck Dashboard', children=[
            html.Div([
                dcc.Graph(id='bar-chart', style={'height': '40vh'}),
                dcc.Graph(id='pie-chart', style={'height': '40vh'}),
                html.Div([
                    html.Div([
                        html.Label(category),
                        dcc.Input(id=f'input-{category.replace(" ", "_")}', type='number', placeholder='Enter Value', value=''),
                        html.Button('Update', id=f'update-button-{category.replace(" ", "_")}', n_clicks=0)
                    ]) for category in df['Category']
                ], style={'margin-bottom': '20px'}),
            ]),
        ]),
        dcc.Tab(label='Total Trucks', children=[
            html.Div([
                html.H2("Total Number of Trucks"),
                html.Div(id='total-trucks-display', style={'font-size': '24px', 'margin-bottom': '20px'}),
                dcc.Input(id='input-total-trucks', type='number', placeholder='Enter Total Trucks', value=''),
                html.Button('Update Total', id='update-button-total', n_clicks=0)
            ])
        ])
    ])
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('total-trucks-display', 'children'),
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

    # Initialize figures to be returned
    bar_fig = create_bar_chart()
    pie_fig = create_pie_chart()

    # Display current total trucks
    total_trucks_display = f"Total Trucks: {total_trucks}"

    if ctx.triggered:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'update-button-total':
            new_total = args[0]
            if new_total is not None and new_total != '':
                total_trucks = int(new_total)
                df['Values'] = 0
                return bar_fig, pie_fig, total_trucks_display, '', *([''] * len(df['Category']))

        for i, category in enumerate(df['Category']):
            if triggered_id == f'update-button-{category.replace(" ", "_")}':
                new_value = args[len(df['Category']) + 2 + i]
                if new_value is not None and new_value != '':
                    value_to_add = int(new_value)
                    if total_trucks >= value_to_add:
                        total_trucks -= value_to_add
                        df.loc[df['Category'] == category, 'Values'] += value_to_add

    # Always return updated figures
    return create_bar_chart(), create_pie_chart(), total_trucks_display, '', *([''] * len(df['Category']))

def create_bar_chart():
    return px.bar(
        df, 
        x='Category', 
        y='Values', 
        title='Bar Chart of Truck Categories',
        color='Category',
        color_discrete_map={
            "Available Trucks": "green",
            "Trucks in Operation": "blue",
            "Waiting Load": "orange",
            "Under Offload": "purple",
            "Breakdown": "red"
        }
    )

def create_pie_chart():
    return px.pie(
        df, 
        values='Values', 
        names='Category', 
        title='Distribution of Truck Categories'
    )

if __name__ == '__main__':
    app.run_server(debug=True)
