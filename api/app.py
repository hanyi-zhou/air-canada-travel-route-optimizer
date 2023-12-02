from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

from program_runner import run_program_with_input

def generate_input_str(selected_cities, selected_routes):
    # Calculate the number of cities and flights
    num_cities = len(selected_cities)
    num_flights = len(selected_routes)

    # Create the input string
    input_str = f"{num_cities} {num_flights}\n"

    # Add city names to the input string
    input_str += "\n".join(selected_cities) + "\n"

    # Add flight routes to the input string
    input_str += "\n".join([f"{city1} {city2}" for city1, city2 in selected_routes]) + "\n"

    return input_str

@app.route('/api/test')
def test():
    return 'Hello, World!'

@app.route('/api/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    selected_cities = data.get('selectedCities', [])
    selected_routes = data.get('selectedRoutes', [])

    input_str = generate_input_str(selected_cities, selected_routes)
    result = run_program_with_input(input_str)

    response_data = {'result': result}
    print(response_data)

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
