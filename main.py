from flask import Flask, request, jsonify
from flask_cors import CORS 
from Nodo import get_siguiente_movimiento
import os

app = Flask(__name__)

CORS(app)

@app.route('/api/tree', methods=['POST'])
def get_tree_result():
    data = request.get_json()
    arreglo_tablero = data.get("arreglo_tablero", [])
    print(arreglo_tablero)
    siguiente_movimiento = get_siguiente_movimiento(arreglo_tablero)

    return jsonify({"posicion": siguiente_movimiento})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
