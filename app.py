import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import callback_context
import base64
import io

app = dash.Dash(__name__)

total_trucks = 0
df = pd.DataFrame({
    "Category": ["Total number of Trucks", "Available Trucks", "Trucks in Operation", "Waiting Load", "Under Offload", "Breakdown"],
    "Values": [0, 0, 0, 0, 0, 0]
})

app.layout = html.Div([
    html.H1("Truck Management Dashboard"),
 html.Div(id='total-trucks', style={'fontSize': 20, 'margin-bottom': '20px'}),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),

    html.Div([
        html.Div([
            html.Label(category),
            dcc.Input(id=f'input-{category}', type='number', placeholder='Enter Value', style={'width': '100px'}),
            html.Button('Update', id=f'update-button-{category}', n_clicks=0, style={'padding': '10px', 'margin-left': '5px'})
        ], style={'margin-bottom': '10px'}) for category in df['Category']
    ], style={'margin-bottom': '20px'}),
    
    html.Button('Download Excel Report', id='download-button', n_clicks=0, style={'padding': '10px', 'margin-top': '20px'}),
    dcc.Download(id='download-dataframe-xlsx')
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('total-trucks', 'children')],
    [Input(f'update-button-{category}', 'n_clicks') for category in df['Category']],
    [Input(f'input-{category}', 'value') for category in df['Category']]
)
def update_chart(*args):
    global df, total_trucks
    
    for i, category in enumerate(df['Category']):
        n_clicks = args[i]
        new_value = args[len(df['Category']) + i]
        if n_clicks > 0 and new_value is not None:
            df.loc[df['Category'] == category, 'Values'] = new_value
            total_trucks -= new_value

    total_text = f"Total Number of Trucks: {total_trucks}"
    
    bar_fig = px.bar(df, x='Category', y='Values', title='Bar Chart of Truck Categories',
                     color='Category',
                     color_discrete_map={
                         "Available Trucks": "green",
                         "Trucks in Operation": "blue",
                         "Waiting Load": "orange",
                         "Under Offload": "purple",
                         "Breakdown": "red"
                     })

    pie_fig = px.pie(df, values='Values', names='Category', title='Distribution of Truck Categories',
                     hole=0.3)

    return bar_fig, pie_fig, total_text

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
