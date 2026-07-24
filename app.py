import random
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Game State
TOTAL_CARTELAS = 150
cartelas = {}
called_numbers = []
current_called_number = None

def generate_cartela_grid():
    # Classic Bingo columns: B(1-15), I(16-30), N(31-45), G(46-60), O(61-75)
    cols = [
        random.sample(range(1, 16), 5),
        random.sample(range(16, 31), 5),
        random.sample(range(31, 46), 5),
        random.sample(range(46, 61), 5),
        random.sample(range(61, 76), 5)
    ]
    grid = [[cols[c][r] for c in range(5)] for r in range(5)]
    grid[2][2] = "FREE"
    return grid

def initialize_game():
    global cartelas, called_numbers, current_called_number
    called_numbers = []
    current_called_number = None
    cartelas = {}
    for i in range(1, TOTAL_CARTELAS + 1):
        cartelas[i] = generate_cartela_grid()

initialize_game()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cartela/<int:cartela_id>', methods=['GET'])
def get_cartela(cartela_id):
    if cartela_id in cartelas:
        return jsonify({"cartela_id": cartela_id, "grid": cartelas[cartela_id]})
    return jsonify({"error": "Cartela not found"}), 404

@app.route('/api/call_number', methods=['POST'])
def call_number():
    global current_called_number, called_numbers
    available = [n for n in range(1, 76) if n not in called_numbers]
    if not available:
        return jsonify({"message": "All numbers called!"}), 400
    
    current_called_number = random.choice(available)
    called_numbers.append(current_called_number)
    
    return jsonify({
        "called_number": current_called_number,
        "total_called": len(called_numbers),
        "history": called_numbers
    })

@app.route('/api/reset', methods=['POST'])
def reset_game():
    initialize_game()
    return jsonify({"message": "Game reset successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

