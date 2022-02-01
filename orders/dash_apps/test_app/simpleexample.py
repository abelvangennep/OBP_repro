import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import datetime as datetime
from datetime import time


from django_plotly_dash import DjangoDash

from orders.models import Analyses, Results
from django_pandas.io import read_frame


app = DjangoDash('SimpleExample')   # replaces dash.Dash

analyses = Analyses.objects.all()
results = Results.objects.all()
df = read_frame(analyses)
df2 = read_frame(results)

def overview(duration,distance,vehicle,production,t_cost,route_cost):
  avg_delivery_time = round(df2[duration].mean(),2)
  avg_prep_and_delivery_time = round(df2[duration].mean() + df2[production].mean(),2)
  avg_distance = round(df2[distance].mean(),2)
  sum_vehicle_cost = round(df2[vehicle].sum(),2)
  avg_cost = round(df2[t_cost].mean(),2)
  avg_route_cost = round(df2[route_cost].mean(),2)

  data_insight = {'Avg distance(m)': avg_distance,
                'Total vehicle cost':sum_vehicle_cost,
                'Avg Total Cost':avg_cost,
                'Avg Route Cost': avg_route_cost}
  
  data_insight_time = {'Avg delivery time': avg_delivery_time,
                'Avg production and delivery time':avg_prep_and_delivery_time}
  
  return data_insight,data_insight_time

overview_first, overview_first_time = overview('first_duration_restaurant', 'first_distance_restaurant','first_min_vehicle_cost', 'first_actual_production_time', 'first_total_cost_restaurant', 'first_route_cost')
overview_second, overview_second_time = overview('second_duration_restaurant', 'second_distance_restaurant', 'second_min_vehicle_cost', 'second_actual_production_time', 'second_total_cost_restaurant', 'second_route_cost')
overview_third, overview_third_time = overview('third_duration_restaurant', 'third_distance_restaurant', 'third_min_vehicle_cost','third_actual_production_time', 'third_total_cost_restaurant', 'third_route_cost')

overview_first['Option'] = 'Option 1'
overview_second['Option'] = 'Option 2'
overview_third['Option'] = 'Option 3'
overview_first_time['Option'] = 'Option 1'
overview_second_time['Option'] = 'Option 2'
overview_third_time['Option'] = 'Option 3'

output = pd.DataFrame()
output_time = pd.DataFrame()

output_time = output_time.append(overview_first_time, ignore_index = True)
output_time = output_time.append(overview_second_time, ignore_index = True)
output_time = output_time.append(overview_third_time, ignore_index = True)

output = output.append(overview_first, ignore_index = True)
output = output.append(overview_second, ignore_index = True)
output = output.append(overview_third, ignore_index = True)


app.layout = html.Div([
    html.H2("Density distributions of perfomance features", style = {'color': 'white'}),
    dcc.Dropdown(id='my-dpdn', multi=False, value='expected_production_time',
                         options=[{'label': 'Expected production time', 'value': 'expected_production_time'},
                         {'label': 'Real production time', 'value': 'real_production'},
                         {'label': 'Delivery time', 'value': 'expected_delivery_time'},
                         {'label': 'Comparing production time with different options', 'value': 'production_time_options'},
                         {'label': 'Comparing route cost with different options', 'value': 'route_cost_options'}]
                         ),
    dcc.Graph(id='fig', figure ={}),
    html.H2('Compare averages between options:', style = {'color': 'white'}),
    dcc.Dropdown(id='my-dpdn2', multi=False, value='first',
                         options=[{'label': 'Average delivery and production time', 'value': 'first'},
                         {'label': 'Average cost', 'value': 'second'},],
                         ),
    dcc.Graph(id = 'fig2', figure = {})
])

@app.callback(
    Output('fig', 'figure'),
    [Input('my-dpdn','value')])

def update_graph(selected_val):
    if selected_val == 'expected_production_time':
        dff = []
        dfff = []
        for x in df['expected_production_time']:
            dff.append(x.hour*60 + x.minute + x.second/60)
        dfff = [dff]
        groups_labels = ['']
        figln = ff.create_distplot(dfff, groups_labels)
    elif selected_val == 'real_production':
        dff = []
        dfff = []
        for x in df['real_production']:
            dff.append(x.hour*60 + x.minute + x.second/60)
        dfff = [dff]
        groups_labels = ['']
        figln = ff.create_distplot(dfff, groups_labels)
    elif selected_val == 'expected_delivery_time':
        dff = []
        dfff = []
        for x in df['expected_delivery_time']:
            dff.append(x.hour*60 + x.minute + x.second/60)
        dfff = [dff]
        groups_labels = ['']
        figln = ff.create_distplot(dfff, groups_labels)
    elif selected_val == 'production_time_options':
        opt_1 = []
        opt_2 = []
        opt_3 = []
        for x in df2['first_actual_production_time']:
            opt_1.append(x)
        for x in df2['second_actual_production_time']:
            opt_2.append(x)
        for x in df2['third_actual_production_time']:
            opt_3.append(x)
        all_opt = [opt_1, opt_2, opt_3]
        print(all_opt)
        group_labels = ['Option 1', 'Option 2', 'Option 3']
        figln = ff.create_distplot(all_opt, group_labels, bin_size =5)
    elif selected_val == 'route_cost_options':
        opt_1 = []
        opt_2 = []
        opt_3 = []
        for x in df2['first_route_cost']:
            opt_1.append(x)
        for x in df2['second_route_cost']:
            opt_2.append(x)
        for x in df2['third_route_cost']:
            opt_3.append(x)
        all_opt = [opt_1, opt_2, opt_3]
        group_labels = ['Option 1', 'Option 2', 'Option 3']
        figln = ff.create_distplot(all_opt, group_labels, bin_size =50)
    return figln

@app.callback(
    Output('fig2', 'figure'),
    [Input('my-dpdn2','value')])

def update_graph(selected_val):
    if selected_val == 'second':
        fig = px.bar(output, x = "Option", y = ["Avg Route Cost", "Avg Total Cost", "Avg distance(m)"], barmode="group")
    elif selected_val == 'first':
        fig = px.bar(output_time, x= "Option", y = ['Avg delivery time', 'Avg production and delivery time'], barmode = "group")
    return fig




   