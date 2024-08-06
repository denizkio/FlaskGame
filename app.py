from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

players = [
    { "name": "Player 1", "inventory": [], "money": 1500 },
    { "name": "Player 2", "inventory": [], "money": 1500 },
    { "name": "Player 3", "inventory": [], "money": 1500 },
    { "name": "Player 4", "inventory": [], "money": 1500 },
]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('gameState', players)

@socketio.on('rollDice')
def handle_roll_dice():
    roll = random.randint(1, 6)
    emit('diceRoll', roll)

@socketio.on('transaction')
def handle_transaction(data):
    players[data['playerIndex']]['money'] += data['amount']
    emit('gameState', players, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
