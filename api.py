from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

current_graph_data = None

@app.route('/concept-map')
def concept_map():
    return app.send_static_file('concept-map.html')

@app.route('/api/graph', methods=['GET', 'POST'])
def handle_graph():
    global current_graph_data
    if request.method == 'POST':
        current_graph_data = request.get_json()
        print(current_graph_data)
        return jsonify({'status': 'success'})
    elif request.method == 'GET':
        return jsonify(current_graph_data)

if __name__ == '__main__':
    app.run(port=5000)