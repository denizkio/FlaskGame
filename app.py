from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

players = [
    { "name": "Player 1", "inventory": [], "money": 1500, "turn": True },
    { "name": "Player 2", "inventory": [], "money": 1500, "turn": False },
    { "name": "Player 3", "inventory": [], "money": 1500, "turn": False },
    { "name": "Player 4", "inventory": [], "money": 1500, "turn": False },
]

cards = [
    { "id": "card1", "type": "resource", "owner": None },
    { "id": "card2", "type": "resource", "owner": None },
    { "id": "card3", "type": "resource", "owner": None },
    { "id": "card4", "type": "resource", "owner": None },
    { "id": "card5", "type": "item", "owner": None },
    { "id": "card6", "type": "item", "owner": None },
    { "id": "card7", "type": "blueprint", "owner": None }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/p<int:player_id>')
def player(player_id):
    return render_template('player.html', player_id=player_id)

@socketio.on('connect')
def handle_connect():
    emit('gameState', {"players": players, "cards": cards})

@socketio.on('rollDice')
def handle_roll_dice(data):
    roll = random.randint(1, 6)
    current_player = data['player_id'] - 1
    players[current_player]['turn'] = False
    next_player = (current_player + 1) % len(players)
    players[next_player]['turn'] = True
    emit('diceRoll', {"roll": roll, "player_id": data['player_id']}, broadcast=True)
    emit('gameState', {"players": players, "cards": cards}, broadcast=True)

@socketio.on('transaction')
def handle_transaction(data):
    players[data['playerIndex']]['money'] += data['amount']
    emit('gameState', {"players": players, "cards": cards}, broadcast=True)

@socketio.on('moveCard')
def handle_move_card(data):
    card_id = data['card_id']
    player_id = data['player_id']
    slot_id = data['slot_id']
    for card in cards:
        if card['id'] == card_id:
            card['owner'] = player_id
            item_in_inventory = next((item for item in players[player_id - 1]['inventory'] if item['cardId'] == card_id), None)
            if item_in_inventory:
                item_in_inventory['slotId'] = slot_id
            else:
                players[player_id - 1]['inventory'].append({"cardId": card_id, "slotId": slot_id})
            break
    emit('gameState', {"players": players, "cards": cards}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
