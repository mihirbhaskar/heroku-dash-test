import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

import pandas as pd

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# app requires "pip install psycopg2" as well

app = dash.Dash(__name__)

# Config the local postgresql database
#app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:M1h1rm@ll@localhost/test"

# Config the Heroku server postgresql database
app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgres://acuyptgxqdqvjv:d34c46c553c1416005aceb276945d98e1902b112946add6a0dd76e040dd5b1de@ec2-54-208-139-247.compute-1.amazonaws.com:5432/d1prugfners9d"


app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app.server)

# Simple layout just displaying the postgres table we have in the server
app.layout = html.Div([
        dcc.Interval(id='interval_pg', interval=1000, n_intervals=0),
        html.Div(id='postgres_datatable')
    ])

# One callback just to pull the table from postgres and output in datatable format
@app.callback(Output('postgres_datatable', 'children'),
              [Input('interval_pg', 'n_intervals')])
def populate_datatable(n_intervals):
    df = pd.read_sql_table('savepandas_mainframe', con=db.engine)
    
    return dash_table.DataTable(id='main_table',
                                columns=[{'name':str(x), 'id':str(x)} for x in df.columns],
                                data = df.to_dict('records'),
                                fixed_rows={'headers': True})
                                
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)