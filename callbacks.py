"""Callback functions for the dashboard"""

from dash import Input, Output
import plotly.express as px
from config import COLOR_SCALE, MONTH_NAMES, MAP_CENTER, MAP_ZOOM
from viz_processing import (
    heatmap_data, 
    weather_overrep_data,
    time_overrep_data,
    month_overrep_data)

def register_callbacks(app):
    """Register all callbacks"""
    
    @app.callback(
        Output('output_plot', 'figure'),
        [Input('mode_selector', 'value'),
         Input('weather_type', 'value'),
         Input('hour_selector', 'value'),
         Input('month_selector', 'value'),
         Input('radius', 'value'),
         Input('min_crashes', 'value'),
         Input('overrep_percentile', 'value')])

    def update_plot(mode, weather_type, selected_hour, selected_month, radius, min_crashes, overrep_percentile):
        """"Create plots from map mode"""

        if mode == 'base':
            plot_data = heatmap_data()
            title_text = "Portland Traffic Incidents Base Heatmap"

        elif mode == 'weather':
            plot_data, expected_prop, total_bins = weather_overrep_data(
                weather_type, min_crashes, overrep_percentile)
            bins_shown = len(plot_data)
            
            if total_bins > 0:
                if bins_shown > 0:
                    title_text = f"{weather_type} Weather Overrepresentation ≥{overrep_percentile}th %ile | Overall {weather_type} Proportion: {expected_prop:.2%} | {bins_shown} locations shown"
                else:
                    title_text = f"{weather_type} Weather Analysis | No locations meet {overrep_percentile}th percentile threshold"
            else:
                title_text = f"{weather_type} Weather Analysis | Insufficient data for analysis"

        elif mode == 'time':
            plot_data, expected_prop, total_bins = time_overrep_data(
                selected_hour, min_crashes, overrep_percentile)
            bins_shown = len(plot_data)
            
            if total_bins > 0:
                if bins_shown > 0:
                    title_text = f"Time Period {selected_hour}:00-{selected_hour}:59 Overrepresentation ≥{overrep_percentile}th %ile | Overall {selected_hour}:00-{selected_hour}:59 Proportion: {expected_prop:.2%} | {bins_shown} locations shown"
                else:
                    title_text = f"Time Period {selected_hour}:00-{selected_hour}:59 Analysis | No locations meet threshold"
            else:
                title_text = f"Time Period {selected_hour}:00-{selected_hour}:59 Analysis | Insufficient data"

        else:  
            plot_data, expected_prop, total_bins = month_overrep_data(
                selected_month, min_crashes, overrep_percentile)
            bins_shown = len(plot_data)
            month_name = MONTH_NAMES[selected_month]
            
            if total_bins > 0:
                if bins_shown > 0:
                    title_text = f"{month_name} Seasonal Analysis ≥{overrep_percentile}th %ile | Overall {month_name} Proportion: {expected_prop:.2%} | {bins_shown} locations shown"
                else:
                    title_text = f"{month_name} Seasonal Analysis | No locations meet threshold"
            else:
                title_text = f"{month_name} Seasonal Analysis | Insufficient data"

        fig = px.density_map(
            plot_data,
            lat="lat_bin",
            lon="lon_bin",
            z="normalized",
            radius=radius,
            color_continuous_scale=COLOR_SCALE,
            center=MAP_CENTER,
            zoom=MAP_ZOOM,
            title=title_text)

        fig.update_layout(
            uirevision="constant",
            map_style="carto-darkmatter",
            margin={"r": 0, "t": 30, "l": 0, "b": 0},
            title={
                'text': title_text,
                'x': 0.5,
                'y': 0.99,  
                'xanchor': 'center',
                'yanchor': 'top', 
                'font': {'size': 18, 'color': 'white', 'family': 'Inter'}},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            autosize=True,
            coloraxis_colorbar=dict(
                title="Incident Density",
                title_font=dict(size=10, family='Inter'),
                tickfont=dict(size=9, family='Inter')))

        fig.update_traces(zmin=0, zmax=1)

        return fig

    @app.callback(
        [Output('weather_controls', 'style'),
         Output('time_controls', 'style'),
         Output('month_controls', 'style'),
         Output('overrep_controls', 'style')],
        Input('mode_selector', 'value'))

    def toggle_controls(mode):
        """Visibility parameters for controls"""

        visible_style = {'marginBottom': '2rem'}
        hidden_style = {'marginBottom': '2rem', 'display': 'none'}
        
        if mode == 'base':
            return hidden_style, hidden_style, hidden_style, hidden_style
        elif mode == 'weather':
            return visible_style, hidden_style, hidden_style, visible_style
        elif mode == 'time':
            return hidden_style, visible_style, hidden_style, visible_style
        else: 
            return hidden_style, hidden_style, visible_style, visible_style