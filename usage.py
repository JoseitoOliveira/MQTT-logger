import eventlet
import sockettest
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from flask import Flask
from flask_socketio import SocketIO
from threading import Timer

eventlet.monkey_patch()
server = Flask(__name__, static_url_path='')
socket = SocketIO(server, async_mode='eventlet')
app = dash.Dash(__name__, server=server)


app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div([
    sockettest.sockettest(),
    html.Progress(id='progress', max=10, value=0),
    dcc.Slider(id='slider', value=0, min=0, max=10, step=1),
    html.Div(id='divspace'),
    html.Div(id='dummy'),
    html.Div(id='dummy1'),
    html.Div(id='dummy2')
])


@app.callback(Output('dummy', 'children'), [Input('progress', 'value')])
def func(value):
    print('progress', value)
    return None


@app.callback(Output('dummy1', 'children'), [Input('divspace', 'children')])
def func(children):
    print('divspace', children)
    return None


@app.callback(Output('dummy2', 'children'), [Input('slider', 'value')])
def func(value):
    print('slider', value)
    return None


def change(id, val):
    socket.emit('call', {'id': id, 'val': val})


def timerCallback():
    Timer(1.0, timerCallback).start()
    change('slider', {'value': timerCallback.i})
    change('progress', {'value': timerCallback.i})
    change('divspace', {'children': 'hello ' + str(timerCallback.i)})
    timerCallback.i += 1
    if timerCallback.i > 10:
        timerCallback.i = 0


timerCallback.i = 0

if __name__ == '__main__':
    timerCallback()
    socket.run(server, debug=True, port=5000, host='0.0.0.0')
