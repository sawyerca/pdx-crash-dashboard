"""Layout components for the webpage"""

from dash import dcc, html
from config import MONTH_NAMES

def create_header():
    """Header section"""

    return html.Div([
        html.Div([
            html.H1("Spatial Analysis of Car Crashes in the Portland Area", 
                   style={
                       'fontSize': '1.75rem',
                       'fontWeight': '600',
                       'margin': '0',
                       'color': 'white'})], 

            style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '0 1.5rem'})], 

        style={
        'background': '#0f172a',
        'color': 'white',
        'height': '70px',
        'display': 'flex',
        'borderBottom': '1px solid #cbd5e1',
        'alignItems': 'center',
        'flexShrink': '0'})

def create_sidebar():
    """Sidebar and controls"""

    return html.Div([

        html.Div([

            html.Div([
                html.H3("Map Mode", style={
                    'color': '#f1f5f9',
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'marginBottom': '0.5rem'}),

                dcc.RadioItems(
                    id='mode_selector',
                    options=[
                        {'label': 'Base Heatmap', 'value': 'base'},
                        {'label': 'Weather Overrepresentation', 'value': 'weather'},
                        {'label': 'Hour Overrepresentation', 'value': 'time'},
                        {'label': 'Month Overrepresentation', 'value': 'month'}],

                    value='base',
                    labelStyle={
                        'display': 'block',
                        'padding': '0.25rem',
                        'backgroundColor': '#0f172a',
                        'borderRadius': '6px',
                        'cursor': 'pointer',
                        'border': '1px solid #475569',
                        'color': '#e2e8f0',
                        'fontSize': '0.875rem',
                        'marginBottom': '0.5rem'})], 

                style={'marginBottom': '1rem'}),


            html.Div(style={'height': '0.125rem'}),

            html.Div([
                html.H3("Select Weather Type", style={
                    'color': '#f1f5f9',
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'marginBottom': '0.5rem'}),

                dcc.RadioItems(
                    id='weather_type',
                    options=[
                        {'label': 'Clear', 'value': 'Clear'},
                        {'label': 'Rainy', 'value': 'Rain'},
                        {'label': 'Cloudy', 'value': 'Cloudy'},
                        {'label': 'Snowy', 'value': 'Snow'}],

                    value='Clear',
                    labelStyle={
                        'display': 'block',
                        'padding': '0.25rem',
                        'backgroundColor': '#0f172a',
                        'borderRadius': '6px',
                        'cursor': 'pointer',
                        'border': '1px solid #475569',
                        'color': '#e2e8f0',
                        'fontSize': '0.875rem',
                        'marginBottom': '0.5rem'})], 

                id='weather_controls', style={'marginBottom': '1rem'}),

            html.Div([
                html.H3("Select Hour of Day", style={
                    'color': '#f1f5f9',
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'marginBottom': '0.5rem'}),

                html.Div([
                    dcc.Slider(
                        id='hour_selector',
                        min=0,
                        max=23,
                        step=1,
                        value=12,
                        marks={0: {'label': '0:00', 'style': {'color': '#cbd5e1', 'fontSize': '10px'}},
                               6: {'label': '6:00', 'style': {'color': '#cbd5e1', 'fontSize': '10px'}},
                               12: {'label': '12:00', 'style': {'color': '#cbd5e1', 'fontSize': '10px'}},
                               18: {'label': '18:00', 'style': {'color': '#cbd5e1', 'fontSize': '10px'}},
                               23: {'label': '23:00', 'style': {'color': '#cbd5e1', 'fontSize': '10px'}}},
                        tooltip={"placement": "bottom", "always_visible": True})], 

                    style={
                    'backgroundColor': '#0f172a',
                    'padding': '1rem',
                    'borderRadius': '2px',
                    'border': '1px solid #475569'})], 

                id='time_controls', style={'marginBottom': '1rem'}),

            html.Div([
                html.H3("Select Month", 
                    style={
                    'color': '#f1f5f9',
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'marginBottom': '0.5rem'}),

                html.Div([
                    dcc.Slider(
                        id='month_selector',
                        min=1,
                        max=12,
                        step=1,
                        value=6,
                        marks={i: {'label': MONTH_NAMES[i][:3], 'style': {'color': '#cbd5e1', 'fontSize': '10px'}} 
                              for i in range(1, 12, 2)},
                        tooltip={"placement": "bottom", "always_visible": True})], 

                    style={
                    'backgroundColor': '#0f172a',
                    'padding': '1rem',
                    'borderRadius': '2px',
                    'border': '1px solid #475569'})], 

                id='month_controls', style={'marginBottom': '1rem'}),

            html.Div([
                html.H3("Map Settings", 
                    style={
                    'color': '#f1f5f9',
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'marginBottom': '0.5rem'}),

                html.Label("Point Influence Radius", 
                    style={
                    'color': '#cbd5e1',
                    'fontSize': '0.8rem',
                    'fontWeight': '500',
                    'marginBottom': '0.5rem',
                    'display': 'block'}),

                html.Div([
                    dcc.Slider(
                        id='radius',
                        min=5,
                        max=50,
                        step=5,
                        value=15,
                        marks={i: {'label': f'{i}', 'style': {'color': '#cbd5e1', 'fontSize': '10px'}} 
                              for i in range(5, 55, 15)},
                        tooltip={"placement": "bottom", "always_visible": True})], 

                    style={
                    'backgroundColor': '#0f172a',
                    'padding': '1rem',
                    'borderRadius': '2px',
                    'border': '1px solid #475569'},
                    title="Controls the radius at which each crash point has influence on density shading")], 

                style={'marginBottom': '1rem'}),

            html.Div([
                html.Label("Minimum Crashes Per Bin", style={
                    'color': '#cbd5e1',
                    'fontSize': '0.8rem',
                    'fontWeight': '500',
                    'marginBottom': '0.5rem',
                    'display': 'block'}),

                html.Div([
                    dcc.Slider(
                        id='min_crashes',
                        min=3,
                        max=20,
                        step=1,
                        value=5,
                        marks={i: {'label': str(i), 'style': {'color': '#cbd5e1', 'fontSize': '10px'}} 
                              for i in [3, 5, 10, 15, 20]},
                        tooltip={"placement": "bottom", "always_visible": True})], 

                    style={
                    'backgroundColor': '#0f172a',
                    'padding': '1rem',
                    'borderRadius': '2px',
                    'border': '1px solid #475569',
                    'marginBottom': '1rem'},
                    title="Controls the minimum number of crashes must be in a bin for that bin to be shown"),

                html.Label("Minimum Overrepresentation Percentile", style={
                    'color': '#cbd5e1',
                    'fontSize': '0.8rem',
                    'fontWeight': '500',
                    'marginBottom': '0.5rem',
                    'display': 'block'}),

                html.Div([
                    dcc.Slider(
                        id='overrep_percentile',
                        min=0,
                        max=99,
                        step=1,
                        value=20,
                        marks={i: {'label': str(i), 'style': {'color': '#cbd5e1', 'fontSize': '10px'}} 
                              for i in [0, 25, 50, 75, 99]},

                        tooltip={"placement": "bottom", "always_visible": True})], 

                    style={
                    'backgroundColor': '#0f172a',
                    'padding': '1rem',
                    'borderRadius': '2px',
                    'border': '1px solid #475569'},
                    title="Hides bins with overrepresentation below selected percentile (calculated after other filters)")], 

                id='overrep_controls', style={'marginBottom': '1rem'})], 

            style={
            'padding': '1rem',
            'height': '100%',
            'overflowY': 'auto',
            'overflowX': 'hidden'})], 

        style={
        'width': '350px',
        'minWidth': '350px',
        'maxWidth': '350px',
        'backgroundColor': '#0e0e0e',
        'borderRight': '1px solid #0f172a',
        'height': '100%',
        'display': 'flex',
        'flexDirection': 'column'})

def create_map():
    """Map section"""

    return html.Div([
        dcc.Graph(
            id='output_plot',
            style={'height': '100%', 'width': '100%'},
            config={
                'responsive': True,
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                'displaylogo': False})], 

        style={
        'flex': '1',
        'backgroundColor': '#0e0e0e',
        'height': '100%'})

def create_app_layout():
    """General app layout"""

    return html.Div([
        create_header(),

        html.Div([
            create_sidebar(),
            create_map()], 

            style={
            'display': 'flex',
            'height': 'calc(100vh - 70px)',
            'overflow': 'hidden'})], 

        style={
        'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        'backgroundColor': '#0e0e0e',
        'color': 'white',
        'height': '100vh',
        'margin': '0',
        'padding': '0',
        'overflow': 'hidden'})