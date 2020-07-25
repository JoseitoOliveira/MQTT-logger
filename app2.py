from threading import Timer

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import eventlet
import pandas as pd
from dash.dependencies import Input, Output
from flask import Flask
from flask_socketio import SocketIO

import sockettest

eventlet.monkey_patch()
server = Flask(__name__, static_url_path='')
socket = SocketIO(server, async_mode='eventlet')
app = dash.Dash(__name__, server=server)


app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})


def generate_table(dataframe, max_rows=100):
    return dash_table.DataTable(id='dt',
                                columns=[{"name": i, "id": i}
                                         for i in dataframe.columns],
                                data=dataframe.to_dict('records'),
                                page_size=30)


app.layout = html.Div(children=[
    sockettest.sockettest(),
    html.H1(children='MQTT Logger'),
    generate_table(df)
])


def change(id, val):
    socket.emit('call', {'id': id, 'val': val})


def timerCallback():
    global df
    Timer(1, timerCallback).start()
    change('dt', {'data': df.to_dict('records')})


if __name__ == '__main__':
    timerCallback()
    socket.run(server, debug=True, port=5000, host='0.0.0.0')
