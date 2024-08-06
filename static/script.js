const socket = io();

document.getElementById('roll-dice').addEventListener('click', () => {
    socket.emit('rollDice', { player_id: playerId });
});

socket.on('diceRoll', (data) => {
    if (data.player_id === playerId) {
        document.getElementById('dice-result').innerText = `Rolled: ${data.roll}`;
    }
});

socket.on('gameState', (data) => {
    const player = data.players[playerId - 1];
    document.getElementById('player-info').innerText = `${player.name}\n$${player.money}`;
    document.getElementById('roll-dice').disabled = !player.turn;

    const centerCardsContainer = document.getElementById('center-cards');
    centerCardsContainer.innerHTML = '';

    data.cards.forEach(card => {
        if (!card.owner) {
            const cardElement = document.createElement('div');
            cardElement.className = `card ${card.type}`;
            cardElement.id = card.id;
            cardElement.draggable = true;
            cardElement.innerText = card.type.charAt(0).toUpperCase() + card.type.slice(1);
            cardElement.addEventListener('dragstart', drag);
            centerCardsContainer.appendChild(cardElement);
        }
    });

    const inventorySlots = document.querySelectorAll('.inventory-slot');
    inventorySlots.forEach(slot => {
        slot.innerHTML = '';
    });

    player.inventory.forEach(item => {
        const card = data.cards.find(c => c.id === item.cardId);
        const cardElement = document.createElement('div');
        cardElement.className = `card ${card.type}`;
        cardElement.id = card.id;
        cardElement.draggable = true;
        cardElement.innerText = card.type.charAt(0).toUpperCase() + card.type.slice(1);
        cardElement.addEventListener('dragstart', drag);
        const targetSlot = document.querySelector(`.inventory-slot[data-slot-id="${item.slotId}"]`);
        if (targetSlot) {
            targetSlot.appendChild(cardElement);
        }
    });
});

function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

function drop(event) {
    event.preventDefault();
    const cardId = event.dataTransfer.getData("text");
    const cardElement = document.getElementById(cardId);
    const slotId = event.target.getAttribute('data-slot-id');
    if (event.target.classList.contains('inventory-slot') && event.target.children.length === 0) {
        event.target.appendChild(cardElement);
        socket.emit('moveCard', { card_id: cardId, player_id: playerId, slot_id: slotId });
    }
}

document.querySelectorAll('.inventory-slot').forEach(slot => {
    slot.addEventListener('drop', drop);
    slot.addEventListener('dragover', allowDrop);
});
