import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import io

app = dash.Dash(__name__)

total_trucks = 0
df = pd.DataFrame({
    "Category": ["Available Trucks", "Trucks in Operation", "Waiting Load", "Under Offload", "Breakdown"],
    "Values": [0, 0, 0, 0, 0]
})

app.layout = html.Div([
    html.H1("Truck Management Dashboard"),
    html.Div([
        html.Div(id='total-trucks', style={'fontSize': 20, 'margin-right': '10px'}),
        dcc.Input(id='input-total-trucks', type='number', placeholder='Enter Total Trucks', style={'width': '100px'}),
        html.Button('Update', id='update-total', n_clicks=0, style={'padding': '10px', 'margin-left': '5px'})
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),
    dcc.Graph(id='bar-chart', style={'height': '300px'}),
    dcc.Graph(id='pie-chart'),
    html.Div([
        html.Div([
            html.Label(category),
            dcc.Input(id=f'input-{category}', type='number', placeholder='Enter Value', style={'width': '100px'}),
            html.Button('Update', id=f'update-button-{category}', n_clicks=0, style={'padding': '10px', 'margin-left': '5px'})
        ], style={'margin-bottom': '10px'}) for category in df['Category']
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-top': '20px'}),
    html.Button('Download Excel Report', id='download-button', n_clicks=0, style={'padding': '10px', 'margin-top': '20px'}),
    dcc.Download(id='download-dataframe-xlsx')
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('total-trucks', 'children'),
     Output('input-total-trucks', 'value')],
    [Input(f'update-button-{category}', 'n_clicks') for category in df['Category']] +
    [Input('update-total', 'n_clicks')],
    [Input(f'input-{category}', 'value') for category in df['Category']] +
    [Input('input-total-trucks', 'value')]
)
def update_chart(*args):
    global df, total_trucks
    trucks_accounted_for = 0

    # Update total trucks if the update button is clicked
    if args[-1] is not None:
        total_trucks = args[-1]

    # Update values for each category
    for i, category in enumerate(df['Category']):
        n_clicks = args[i]
        new_value = args[len(df['Category']) + i]
        if n_clicks > 0 and new_value is not None:
            df.loc[df['Category'] == category, 'Values'] = new_value
            trucks_accounted_for += new_value

    remaining_trucks = total_trucks - trucks_accounted_for
    total_text = f"Total Number of Trucks: {remaining_trucks}"

    # Create bar chart
    bar_fig = px.bar(df, x='Category', y='Values', title='Bar Chart of Truck Categories',
                     color='Category',
                     color_discrete_map={
                         "Available Trucks": "green",
                         "Trucks in Operation": "blue",
                         "Waiting Load": "orange",
                         "Under Offload": "purple",
                         "Breakdown": "red"
                     })
    bar_fig.update_layout(height=300)  # Reduced bar chart height

    # Create pie chart
    pie_fig = px.pie(df, values='Values', names='Category', title='Distribution of Truck Categories',
                     hole=0.3)
    
    return bar_fig, pie_fig, total_text, None  # Clear the input field for total trucks

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_xlsx(n_clicks):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Truck Data', index=False)
        writer.save()
        output.seek(0)
    return dict(content=output.getvalue(), filename="truck_data.xlsx")

if __name__ == '__main__':
    app.run_server(debug=True)

application = app.server
