"""Main application file"""

import dash
import os
from config import EXTERNAL_STYLESHEETS, INDEX_STRING
from layout import create_app_layout
from callbacks import register_callbacks
from viz_processing import load_crashes

#LOAD/REGISTER/ETC

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
server = app.server

app.index_string = INDEX_STRING

load_crashes()

app.layout = create_app_layout()

register_callbacks(app)

#RUN

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False)