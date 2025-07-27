"""Data loading and preprocessing for the dashboard."""

import pandas as pd
import numpy as np


#GLOBAL VARS

portland_crashes = None
weather_data = None
hour_data = None
month_data = None
global_weather_props = None
global_hour_props = None
global_month_props = None


#DATA PROCESSING FOR VIZ

def load_crashes():
    """Loading and preprocessing"""

    global portland_crashes, weather_data, hour_data, month_data
    global global_weather_props, global_hour_props, global_month_props
    
    portland_crashes = pd.read_csv('portland_crashes.CSV')

    weather_data = portland_crashes[
        portland_crashes['WTHR_COND_SHORT_DESC'].str.contains('CLR|RAIN|CLD|SNOW',
            case=False, na=False)].copy()

    weather_data['weather_type'] = weather_data['WTHR_COND_SHORT_DESC'].apply(lambda x:
        'Clear' if 'CLR' in str(x).upper() else
        'Rain' if 'RAIN' in str(x).upper() else
        'Cloudy' if 'CLD' in str(x).upper() else
        'Snow' if 'SNOW' in str(x).upper() else
        'Other')

    weather_data = weather_data[weather_data['weather_type'] != 'Other']

    global_weather_props = weather_data['weather_type'].value_counts(normalize=True)

    hour_data = portland_crashes.dropna(subset=['CRASH_HR_NO']).copy()
    global_hour_props = hour_data['CRASH_HR_NO'].value_counts(normalize=True).sort_index()

    month_data = portland_crashes.dropna(subset=['CRASH_MO_NO']).copy()
    global_month_props = month_data['CRASH_MO_NO'].value_counts(normalize=True).sort_index()

def heatmap_data():
    """Data for the base heatmap"""

    df = portland_crashes.copy()
    df['lat_bin'] = df['LAT_DD'].round(5)
    df['lon_bin'] = df['LONGTD_DD'].round(4)
    grouped = df.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='count')
    grouped['log_count'] = np.log1p(grouped['count'])

    min_val = grouped['log_count'].min()
    max_val = grouped['log_count'].max()
    if max_val > min_val:
        grouped['normalized'] = (grouped['log_count'] - min_val) / (max_val - min_val)
    else:
        grouped['normalized'] = 0

    return grouped

def weather_overrep_data(weather_type, min_crashes, overrep_percentile):
    """Data for weather overrepresentation"""

    expected_prop = global_weather_props[weather_type]
    bin_size = 0.00001  

    decimal_places = max(1, int(-np.log10(bin_size)))
    weather_data_copy = weather_data.copy()
    weather_data_copy['lat_bin'] = weather_data_copy['LAT_DD'].round(decimal_places)
    weather_data_copy['lon_bin'] = weather_data_copy['LONGTD_DD'].round(decimal_places)

    total_by_bin = weather_data_copy.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='total_crashes')

    weather_specific = weather_data_copy[weather_data_copy['weather_type'] == weather_type]
    weather_by_bin = weather_specific.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='weather_crashes')

    merged = total_by_bin.merge(weather_by_bin, on=['lat_bin', 'lon_bin'], how='left')
    merged['weather_crashes'] = merged['weather_crashes'].fillna(0)

    merged['local_proportion'] = merged['weather_crashes'] / merged['total_crashes']

    merged = merged[merged['local_proportion'] > expected_prop].copy()
    merged = merged[merged['total_crashes'] >= min_crashes].copy()

    if len(merged) > 0:
        merged['overrep_proportion'] = merged['local_proportion'] / expected_prop
        
        merged_sorted = merged.sort_values('overrep_proportion')
        n_bins = len(merged_sorted)
        
        if n_bins > 1:
            cutoff_rank = int(np.ceil((overrep_percentile / 100) * n_bins))
            cutoff_rank = max(1, cutoff_rank)  
            plot_data = merged_sorted.tail(n_bins - cutoff_rank + 1).copy()
        else:
            plot_data = merged.copy()

        if len(plot_data) > 0:
            plot_data['intensity'] = plot_data['overrep_proportion']
            
            min_val = plot_data['intensity'].min()
            max_val = plot_data['intensity'].max()
            if max_val > min_val:
                plot_data['normalized'] = (plot_data['intensity'] - min_val) / (max_val - min_val)
            else:
                plot_data['normalized'] = 0.5
        else:
            plot_data['normalized'] = []
    else:
        plot_data = pd.DataFrame(columns=['lat_bin', 'lon_bin', 'normalized'])

    return plot_data, expected_prop, len(merged)

def time_overrep_data(selected_hour, min_crashes, overrep_percentile):
    """Data for time overrepresentation"""

    expected_prop = global_hour_props[selected_hour]
    bin_size = 0.00001  

    decimal_places = max(1, int(-np.log10(bin_size)))
    hour_data_copy = hour_data.copy()
    hour_data_copy['lat_bin'] = hour_data_copy['LAT_DD'].round(decimal_places)
    hour_data_copy['lon_bin'] = hour_data_copy['LONGTD_DD'].round(decimal_places)

    total_by_bin = hour_data_copy.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='total_crashes')

    hour_specific = hour_data_copy[hour_data_copy['CRASH_HR_NO'] == selected_hour]
    hour_by_bin = hour_specific.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='hour_crashes')

    merged = total_by_bin.merge(hour_by_bin, on=['lat_bin', 'lon_bin'], how='left')
    merged['hour_crashes'] = merged['hour_crashes'].fillna(0)

    merged['local_proportion'] = merged['hour_crashes'] / merged['total_crashes']

    merged = merged[merged['local_proportion'] > expected_prop].copy()
    merged = merged[merged['total_crashes'] >= min_crashes].copy()

    if len(merged) > 0:
        merged['overrep_proportion'] = merged['local_proportion'] / expected_prop
        
        merged_sorted = merged.sort_values('overrep_proportion')
        n_bins = len(merged_sorted)
        
        if n_bins > 1:
            cutoff_rank = int(np.ceil((overrep_percentile / 100) * n_bins))
            cutoff_rank = max(1, cutoff_rank)
            plot_data = merged_sorted.tail(n_bins - cutoff_rank + 1).copy()
        else:
            plot_data = merged.copy()

        if len(plot_data) > 0:
            plot_data['intensity'] = plot_data['overrep_proportion']
            
            min_val = plot_data['intensity'].min()
            max_val = plot_data['intensity'].max()
            if max_val > min_val:
                plot_data['normalized'] = (plot_data['intensity'] - min_val) / (max_val - min_val)
            else:
                plot_data['normalized'] = 0.5
        else:
            plot_data['normalized'] = []
    else:
        plot_data = pd.DataFrame(columns=['lat_bin', 'lon_bin', 'normalized'])

    return plot_data, expected_prop, len(merged)

def month_overrep_data(selected_month, min_crashes, overrep_percentile):
    """Data for month overrepresentation"""

    expected_prop = global_month_props[selected_month]
    bin_size = 0.00001  

    decimal_places = max(1, int(-np.log10(bin_size)))
    month_data_copy = month_data.copy()
    month_data_copy['lat_bin'] = month_data_copy['LAT_DD'].round(decimal_places)
    month_data_copy['lon_bin'] = month_data_copy['LONGTD_DD'].round(decimal_places)

    total_by_bin = month_data_copy.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='total_crashes')

    month_specific = month_data_copy[month_data_copy['CRASH_MO_NO'] == selected_month]
    month_by_bin = month_specific.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='month_crashes')

    merged = total_by_bin.merge(month_by_bin, on=['lat_bin', 'lon_bin'], how='left')
    merged['month_crashes'] = merged['month_crashes'].fillna(0)

    merged['local_proportion'] = merged['month_crashes'] / merged['total_crashes']

    merged = merged[merged['local_proportion'] > expected_prop].copy()
    merged = merged[merged['total_crashes'] >= min_crashes].copy()

    if len(merged) > 0:
        merged['overrep_proportion'] = merged['local_proportion'] / expected_prop
        
        merged_sorted = merged.sort_values('overrep_proportion')
        n_bins = len(merged_sorted)
        
        if n_bins > 1:
            cutoff_rank = int(np.ceil((overrep_percentile / 100) * n_bins))
            cutoff_rank = max(1, cutoff_rank)  
            plot_data = merged_sorted.tail(n_bins - cutoff_rank + 1).copy()
        else:
            plot_data = merged.copy()

        if len(plot_data) > 0:
            plot_data['intensity'] = plot_data['overrep_proportion']
            
            min_val = plot_data['intensity'].min()
            max_val = plot_data['intensity'].max()
            if max_val > min_val:
                plot_data['normalized'] = (plot_data['intensity'] - min_val) / (max_val - min_val)
            else:
                plot_data['normalized'] = 0.5
        else:
            plot_data['normalized'] = []
    else:
        plot_data = pd.DataFrame(columns=['lat_bin', 'lon_bin', 'normalized'])

    return plot_data, expected_prop, len(merged)