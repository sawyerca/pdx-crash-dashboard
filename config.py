"""Configuration and constants for the dashboard"""


#NAMES/SCALES

MONTH_NAMES = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'}

COLOR_SCALE = [
    [0, "rgba(16, 185, 129, 0.0)"],      
    [0.25, "rgba(34, 197, 94, 0.8)"],
    [0.5, "rgba(251, 191, 36, 0.8)"],  
    [0.75, "rgba(249, 115, 22, 0.8)"],
    [1, "rgba(239, 68, 68, 0.9)"]]


#STYLING

EXTERNAL_STYLESHEETS = [
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap']

INDEX_STRING = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


#MAP STATE

MAP_CENTER = dict(lat=45.45, lon=-122.6784)
MAP_ZOOM = 10