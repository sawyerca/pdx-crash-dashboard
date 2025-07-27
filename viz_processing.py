"""Data loading and preprocessing for the dashboard"""

import pandas as pd
import numpy as np

#Global Vars
portland_crashes = None
global_weather_props = None
global_hour_props = None
global_month_props = None
bin_size = 0.00001

def load_crashes():
    """Loading and preprocessing"""

    global portland_crashes, global_weather_props, global_hour_props, global_month_props
    
    dtypes = {
        'LAT_DD': 'float32',
        'LONGTD_DD': 'float32', 
        'CRASH_HR_NO': 'int8',
        'CRASH_MO_NO': 'int8'}
    
    needed_cols = ['LAT_DD', 'LONGTD_DD', 'WTHR_COND_SHORT_DESC', 'CRASH_HR_NO', 'CRASH_MO_NO']
    portland_crashes = pd.read_csv('portland_crashes.CSV', dtype=dtypes, usecols=needed_cols)
    
    portland_crashes = portland_crashes.dropna(subset=['LAT_DD', 'LONGTD_DD'])
    
    weather_mask = portland_crashes['WTHR_COND_SHORT_DESC'].str.contains('CLR|RAIN|CLD|SNOW', case=False, na=False)
    weather_subset = portland_crashes[weather_mask].copy()
    
    weather_subset['weather_type'] = weather_subset['WTHR_COND_SHORT_DESC'].apply(lambda x:
        'Clear' if 'CLR' in str(x).upper() else
        'Rain' if 'RAIN' in str(x).upper() else
        'Cloudy' if 'CLD' in str(x).upper() else
        'Snow' if 'SNOW' in str(x).upper() else
        'Other')
    
    weather_subset = weather_subset[weather_subset['weather_type'] != 'Other']
    global_weather_props = weather_subset['weather_type'].value_counts(normalize=True)
    
    hour_subset = portland_crashes.dropna(subset=['CRASH_HR_NO'])
    global_hour_props = hour_subset['CRASH_HR_NO'].value_counts(normalize=True).sort_index()
    
    month_subset = portland_crashes.dropna(subset=['CRASH_MO_NO'])
    global_month_props = month_subset['CRASH_MO_NO'].value_counts(normalize=True).sort_index()
        


def heatmap_data():
    """Data for the base heatmap"""

    decimal_places = max(1, int(-np.log10(bin_size)))

    df = portland_crashes[['LAT_DD', 'LONGTD_DD']].copy()
    df['lat_bin'] = df['LAT_DD'].round(decimal_places)
    df['lon_bin'] = df['LONGTD_DD'].round(decimal_places)
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
    
    weather_mask = portland_crashes['WTHR_COND_SHORT_DESC'].str.contains('CLR|RAIN|CLD|SNOW', case=False, na=False)
    weather_df = portland_crashes[weather_mask]
    
    if weather_type == 'Clear':
        condition_mask = weather_df['WTHR_COND_SHORT_DESC'].str.contains('CLR', case=False, na=False)
    elif weather_type == 'Rain':
        condition_mask = weather_df['WTHR_COND_SHORT_DESC'].str.contains('RAIN', case=False, na=False)
    elif weather_type == 'Cloudy':
        condition_mask = weather_df['WTHR_COND_SHORT_DESC'].str.contains('CLD', case=False, na=False)
    else:  
        condition_mask = weather_df['WTHR_COND_SHORT_DESC'].str.contains('SNOW', case=False, na=False)
    
    return process_overrep(weather_df, condition_mask, expected_prop, min_crashes, overrep_percentile)

def time_overrep_data(selected_hour, min_crashes, overrep_percentile):
    """Data for time overrepresentation"""

    expected_prop = global_hour_props[selected_hour]
    hour_df = portland_crashes.dropna(subset=['CRASH_HR_NO'])
    condition_mask = hour_df['CRASH_HR_NO'] == selected_hour
    
    return process_overrep(hour_df, condition_mask, expected_prop, min_crashes, overrep_percentile)

def month_overrep_data(selected_month, min_crashes, overrep_percentile):
    """Data for month overrepresentation"""

    expected_prop = global_month_props[selected_month]
    month_df = portland_crashes.dropna(subset=['CRASH_MO_NO'])
    condition_mask = month_df['CRASH_MO_NO'] == selected_month
    
    return process_overrep(month_df, condition_mask, expected_prop, min_crashes, overrep_percentile)

def process_overrep(df, condition_mask, expected_prop, min_crashes, overrep_percentile):
    """Helper function to process overrepresentation"""

    decimal_places = max(1, int(-np.log10(bin_size)))
    
    lat_bins = df['LAT_DD'].round(decimal_places)
    lon_bins = df['LONGTD_DD'].round(decimal_places)
    
    total_counts = pd.DataFrame({'lat_bin': lat_bins, 'lon_bin': lon_bins}).groupby(['lat_bin', 'lon_bin']).size()
    
    condition_df = df[condition_mask]
    if len(condition_df) > 0:
        condition_lat_bins = condition_df['LAT_DD'].round(decimal_places)
        condition_lon_bins = condition_df['LONGTD_DD'].round(decimal_places)
        condition_counts = pd.DataFrame({'lat_bin': condition_lat_bins, 'lon_bin': condition_lon_bins}).groupby(['lat_bin', 'lon_bin']).size()
    else:
        condition_counts = pd.Series(dtype='int64')
    
    merged = total_counts.to_frame('total_crashes').join(condition_counts.to_frame('condition_crashes'), how='left')
    merged['condition_crashes'] = merged['condition_crashes'].fillna(0)
    merged['local_proportion'] = merged['condition_crashes'] / merged['total_crashes']
    
    merged = merged[merged['local_proportion'] > expected_prop]
    merged = merged[merged['total_crashes'] >= min_crashes]
    
    if len(merged) > 0:
        merged['overrep_proportion'] = merged['local_proportion'] / expected_prop
        
        cutoff_rank = int(np.ceil((overrep_percentile / 100) * len(merged)))
        cutoff_rank = max(1, cutoff_rank)
        plot_data = merged.nlargest(len(merged) - cutoff_rank + 1, 'overrep_proportion').reset_index()
        
        if len(plot_data) > 0:
            min_val = plot_data['overrep_proportion'].min()
            max_val = plot_data['overrep_proportion'].max()
            if max_val > min_val:
                plot_data['normalized'] = (plot_data['overrep_proportion'] - min_val) / (max_val - min_val)
            else:
                plot_data['normalized'] = 0.5
        else:
            plot_data = pd.DataFrame(columns=['lat_bin', 'lon_bin', 'normalized'])
    else:
        plot_data = pd.DataFrame(columns=['lat_bin', 'lon_bin', 'normalized'])

    return plot_data, expected_prop, len(merged)