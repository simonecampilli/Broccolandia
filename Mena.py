import numpy as np
import pandas as pd
import geopy.distance
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import geodesic
from scipy.spatial.distance import pdist, squareform

# 1. Read the Excel file
df = pd.read_excel('Report_Complessivo_AqA_blocco35_Apr.mag.24.xlsx')
df = df.dropna(subset=['Latitude', 'Longitude'])

# 2. Function to calculate the distance between two coordinates
def calcola_distanza(coord1, coord2):
    return geodesic(coord1, coord2).km

# 3. Create the data model for the VRP
def create_data_model(group):
    # Depot coordinates
    #punto0 = [[45.1554427, 10.7978819]]
    punti = group[['Latitude', 'Longitude']].values
    # Add the depot to the list of points
    #punti = np.vstack([punto0, punti])
    data = {}
    # Calculate the geodesic distance matrix (in km)
    dist_matrix = squareform(pdist(punti, lambda u, v: geodesic(u, v).kilometers))
    # Convert distances to meters and cast to integers
    data['distance_matrix'] = (dist_matrix * 1000).astype(int)
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

# 4. Function to calculate routes minimizing total distance using up to 5 vehicles
def calcola_percorsi(group):
    data = create_data_model(group)

    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data['num_vehicles'], data['depot']
    )

    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback
    def distance_callback(from_index, to_index):
        """Returns the distance between two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC
    )
    # Set a time limit (in seconds)
    search_parameters.time_limit.FromSeconds(30)

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console
    if solution:
        return print_solution(data, manager, routing, solution, group)
    else:
        print("No solution found!")
        return 0

# 5. Function to print the solution
def print_solution(data, manager, routing, solution, gruppo):
    """Prints solution on console."""
    total_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        if routing.IsEnd(index):
            continue  # Skip unused vehicles
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            plan_output += f" {node_index} ->"
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            if not routing.IsEnd(index):
                route_distance += data['distance_matrix'][manager.IndexToNode(previous_index)][manager.IndexToNode(index)]
        plan_output += f" {manager.IndexToNode(index)}\n"
        plan_output += f"Distance of the route: {route_distance / 1000:.2f} km\n"
        print(plan_output)
        total_distance += route_distance
    print(f"Total distance of all routes: {total_distance / 1000:.2f} km")
    return total_distance

# 6. Function to compare current and proposed methods
def calcola_primi_100_consumo_attuale(df1):
    punti = df1[['Latitude', 'Longitude']].values
    emissioni_totali = 0
    distanza = 0
    # Calculate emissions and distance for the current method
    for i in range(1, len(punti)):

        distanza_km = calcola_distanza(punti[i - 1], punti[i])
        print(i, punti[i - 1], punti[i],distanza_km)
        emissioni_totali += distanza_km * 120 / 1000  # Emissions in kg
        distanza += distanza_km
    # Calculate emissions and distance for the proposed method
    dist_prop_meters = calcola_percorsi(df1)
    dist_prop_km = dist_prop_meters / 1000
    emissioni_proposte = dist_prop_km * 120 / 1000  # Emissions in kg
    print('Metodo proposto:', emissioni_proposte, 'kg CO₂ per una distanza di km:', dist_prop_km)
    print('Metodo attuale:', emissioni_totali, 'kg CO₂ per una distanza di km:', distanza)
df['Data Lettura'] = pd.to_datetime(df['Data Lettura'], errors='coerce', dayfirst=True)

# Filter the DataFrame for rows where 'Data Lettura' is 02/05 (May 2nd)
specific_date = '2024-05-02'  # Adjust the year if needed
df_filtered = df[(df['Data Lettura'] == specific_date) & (df['Codice Letturista'] == 'LO0414')]
df_sorted = df_filtered.sort_values(by='Ora Lettura')
# Group by the 'Data Lettura' column (though this will contain only one group now)
#gruppi = df_filtered.groupby(['Data Lettura'])
# 7. Execute the comparison
#gruppi=df.groupby(['Data Lettura'])
#for (data),gruppo in gruppi:
calcola_primi_100_consumo_attuale(df_sorted)
