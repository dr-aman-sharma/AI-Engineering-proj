# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                       2500: '2500',
                                       5000: '5000',
                                       7500: '7500',
                                       10000: '10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # For all sites, show total successful launches vs failed launches
        success_counts = spacex_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        success_counts['outcome'] = success_counts['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(success_counts, values='count', names='outcome', 
                     title='Total Launch Outcomes for All Sites',
                     color='outcome',
                     color_discrete_map={'Success': 'green', 'Failure': 'red'})
        return fig
    else:
        # Filter data for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count success and failure for the selected site
        site_counts = filtered_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        site_counts['outcome'] = site_counts['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(site_counts, values='count', names='outcome',
                     title=f'Launch Outcomes for {entered_site}',
                     color='outcome',
                     color_discrete_map={'Success': 'green', 'Failure': 'red'})
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    # Filter data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        # For all sites, show all data points
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs Launch Outcome for All Sites',
                         labels={'class': 'Launch Outcome (0=Failure, 1=Success)',
                                'Payload Mass (kg)': 'Payload Mass (kg)'},
                         hover_data=['Launch Site'])
        # Update y-axis to show discrete values
        fig.update_yaxes(tickvals=[0, 1], ticktext=['Failure', 'Success'])
        return fig
    else:
        # Filter for specific site
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs Launch Outcome for {entered_site}',
                         labels={'class': 'Launch Outcome (0=Failure, 1=Success)',
                                'Payload Mass (kg)': 'Payload Mass (kg)'},
                         hover_data=['Launch Site'])
        # Update y-axis to show discrete values
        fig.update_yaxes(tickvals=[0, 1], ticktext=['Failure', 'Success'])
        return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)