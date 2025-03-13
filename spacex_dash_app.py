# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),
    
    # TASK 1: Launch site dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
        ],
        value='All Sites',  # default value
        placeholder="Select a Launch Site",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Success pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Payload range slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={i: str(i) for i in range(int(min_payload), int(max_payload)+1, 1000)},
        value=[min_payload, max_payload]  # default value for slider
    ),
    # TASK 4: Success vs Payload scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback to update the pie chart based on the selected site
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'All Sites':
        site_data = spacex_df
    else:
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]

    success_counts = site_data['class'].value_counts()
    fig = px.pie(
        success_counts,
        values=success_counts,
        names=['Failure', 'Success'],
        title=f"Launch Success for {selected_site}" if selected_site != 'All Sites' else "Total Launch Success"
    )
    return fig

# TASK 4: Callback to update the scatter chart based on selected site and payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    min_payload, max_payload = payload_range

    if selected_site == 'All Sites':
        scatter_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) &
                                 (spacex_df['Payload Mass (kg)'] <= max_payload)]
    else:
        scatter_data = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                 (spacex_df['Payload Mass (kg)'] >= min_payload) &
                                 (spacex_df['Payload Mass (kg)'] <= max_payload)]

    fig = px.scatter(
        scatter_data,
        x='Payload Mass (kg)',
        y='class',
        color='class',
        title=f"Launch Success vs Payload for {selected_site}" if selected_site != 'All Sites' else "Launch Success vs Payload for All Sites",
        labels={'class': 'Success (1) / Failure (0)'}
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
