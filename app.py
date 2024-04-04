# %% [markdown]
# ### Sprint #4: Dashboard V0
# 
# DS4003 | Spring 2024
# 
# The objective of this sprint id to begin the dashboard build.
# 
# **Instructions**
# 
# Start coding your dashboard. You may begin with whatever elements you prefer. The sprint deliverable must include at least one graph/data table with two UI components (radio button, slider, etc). The graph does not need to be in final form, but needs to have all the basic elements and styling in place.
# 
# **Deliverables**
# 
# URL to Github Repo with Render URL in the readme

# %%
# importing dependencies
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

# %%
# read in and view dataframe
df = pd.read_csv("data.csv")
df.head()

# %%
# load the CSS stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# %%
# initialize the app
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

# %%
# creating layout 
app.layout = html.Div([
    # add title and description
    html.H2("Countries' Carbon Dioxide (CO2) Emissions from 1990 - 2022 by Metric Tons"),
    html.H5("This dashboard is meant to be a way to track carbon dioxide (CO2) by country by its primary ways of being released into the atmosphere via fossil fuels over a period of time from 1990 to 2022. Carbon dioxide is a greenhouse that traps heat in the earth's atmosphere contributing to global warming and climate change. With carbon dioxide concentrations inceasing rapidly and the temperature alarmingly rising, I think that it is important to understand who and what the most significant contributers are. The data selected is was published by researchers from the Center for International Climate Research (CICERO) using the most recent 2023 release of the Global Carbon Project (GCP) fossil emissions dataset." ),
    # layout elements
    html.Div([
        html.Div([
            # create dropdown menu to select countries with preselected values to avoid error
            html.Label('Select Countries'),
            dcc.Dropdown(
                options=[{'label': country, 'value': country} for country in df['country'].unique()],
                id='country-dropdown',
                value=['Algeria','United Kingdom'],
                multi=True
            ),
        ],
         #changing format so that it takes up one third  page and looks cohesive
          style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),

        html.Div([
            # create dropdown menu to select types  with preselected value to avoid error
            html.Label('Select CO2 Emission Type'),
            dcc.Dropdown(
                options=[{'label': col, 'value': col} for col in df.columns[2:9]],
                id='co2-dropdown',
                value=['oil'],
                multi=False
            ),
        ],
         # changing format so that it takes up one thrid of page  and looks cohesive
          style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),
         
        html.Div([
            # create slider to select year with preselected values to avoid error & also dividing slider into increments
            dcc.RangeSlider(
                min=int(df['year'].min()),
                max=int(df['year'].max()),  
                step=None, 
                id='year-range-slider',
                marks = {str(year): str(year) for year in range(df['year'].min(), df['year'].max() + 1, 8)},
                value=[2010, 2020]
            ) , 
        ],
        # changing format to one third of page
          style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'bottom'})
        ]),
        # co2 graph
        dcc.Graph(id='co2-graph')
])
# define callbacks/update graph function        
@app.callback(
    Output('co2-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('co2-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
def update_graph(selected_countries, selected_types, selected_years):
    # filtering dataframe
    filtered_df = df[(df['country'].isin(selected_countries)) & 
                     (df['year'] >= selected_years[0]) & 
                     (df['year'] <= selected_years[1])]
    
    # making graph
    fig = px.line(filtered_df,
                  x='year', # years on x axis
                  y=selected_types,  # user selected type here
                  title='CO2 Emissions Over Time for Selected Countries',
                  color='country',  # Each country will be represented by a different color
                  markers=True  # Show markers at data points
                 )
    fig.update_layout(
        title='CO2 Emissions Over Time for Selected Countries',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions for Selected Type by Metric Tons',
    )
    return fig
#run app
if __name__ == '__main__':
    app.run_server(debug=True)


