from api.program_runner import run_program_with_input

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

# Example usage:
selected_cities = ["Vancouver", "Yellowknife", "Edmonton", "Calgary", "Winnipeg", "Toronto", "Montreal", "Halifax"]
selected_routes = [("Vancouver", "Edmonton"), ("Vancouver", "Calgary"), ("Calgary", "Winnipeg"),
                   ("Winnipeg", "Toronto"), ("Toronto", "Halifax"), ("Montreal", "Halifax"),
                   ("Edmonton", "Montreal"), ("Edmonton", "Yellowknife"), ("Edmonton", "Calgary")]

input_str = generate_input_str(selected_cities, selected_routes)

def process_function(input_str):
    result = run_program_with_input(input_str)
    return result
