import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from geopy.distance import geodesic

# **1. Caricamento e Pulizia dei Dati**

# Percorso del file dei dati
data_path = 'Report_Complessivo_AqA_blocco35_Apr.mag.24.xlsx'  # Modifica con il percorso del tuo file

# Carica i dati dal foglio 'Letture'
data = pd.read_excel(data_path, sheet_name='Letture')

# Seleziona le colonne necessarie e rimuovi duplicati e valori mancanti
coordinates = data[['Latitude', 'Longitude']].dropna().drop_duplicates().reset_index(drop=True)

# **2. Clusterizzazione dei Punti**

# Numero di cluster (da regolare in base alle esigenze)
num_clusters = 100

# Applica K-Means per creare cluster geografici
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
coordinates['Cluster'] = kmeans.fit_predict(coordinates[['Latitude', 'Longitude']])

# **3. Definizione delle Funzioni per l'Ottimizzazione**

# Funzione per risolvere il TSP utilizzando Google OR-Tools
def solve_tsp(distance_matrix):
    tsp_size = len(distance_matrix)
    num_routes = 1  # Un solo veicolo per cluster
    depot = 0  # Punto di partenza (primo punto del cluster)

    # Crea il gestore dei dati
    manager = pywrapcp.RoutingIndexManager(tsp_size, num_routes, depot)

    # Crea il modello di routing
    routing = pywrapcp.RoutingModel(manager)

    # Funzione di distanza tra nodi
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node])

    # Registra la funzione di distanza
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Imposta i parametri di ricerca
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 30  # Limite di tempo per la ricerca

    # Risolve il problema
    solution = routing.SolveWithParameters(search_parameters)

    # Estrae il percorso ottimizzato
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))  # Aggiungi il punto finale
        return route
    else:
        return None

# Funzione per calcolare le emissioni di CO2
def calculate_co2_emissions(total_distance_km, emission_factor=0.192):
    """
    Calcola le emissioni di CO2.
    :param total_distance_km: Distanza totale in chilometri.
    :param emission_factor: Fattore di emissione in kg CO2 per km (valore medio per veicoli a benzina).
    :return: Emissioni totali di CO2 in kg.
    """
    return total_distance_km * emission_factor

# **4. Ottimizzazione dei Percorsi per Tutti i Cluster**

optimized_routes = {}
total_distance = 0

for cluster_id in range(num_clusters):
    cluster_data = coordinates[coordinates['Cluster'] == cluster_id].reset_index(drop=True)
    cluster_points = cluster_data[['Latitude', 'Longitude']].to_numpy()
    num_points = len(cluster_points)

    if num_points > 1:
        # Crea la matrice delle distanze geodetiche
        distance_matrix = np.zeros((num_points, num_points))
        for i in range(num_points):
            for j in range(num_points):
                if i != j:
                    # Calcola la distanza in metri tra i punti
                    distance_matrix[i][j] = geodesic(cluster_points[i], cluster_points[j]).meters
                else:
                    distance_matrix[i][j] = 0

        # Risolvi il TSP per il cluster corrente
        route = solve_tsp(distance_matrix)
        if route:
            optimized_routes[cluster_id] = route

            # Calcola la distanza totale per il cluster in km
            cluster_distance = sum(
                geodesic(cluster_points[route[i]], cluster_points[route[i + 1]]).kilometers
                for i in range(len(route) - 1)
            )
            total_distance += cluster_distance
        else:
            print(f"Soluzione non trovata per il cluster {cluster_id}")
    else:
        print(f"Cluster {cluster_id} ha un solo punto.")

# **5. Calcolo Totale delle Emissioni di CO2**

# Calcola le emissioni totali di CO2
total_co2_emissions = calculate_co2_emissions(total_distance)
print(f"Distanza totale percorsa: {total_distance:.2f} km")
print(f"Emissioni totali di CO2: {total_co2_emissions:.2f} kg")

# **6. Visualizzazione dei Percorsi Ottimizzati**

def plot_optimized_route(cluster_id, cluster_data, optimized_route):
    plt.figure(figsize=(10, 8))
    optimized_points = cluster_data.iloc[optimized_route]
    plt.plot(optimized_points['Longitude'], optimized_points['Latitude'], 'o-', label=f'Cluster {cluster_id}')
    plt.title(f'Percorso ottimizzato per il Cluster {cluster_id}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.legend()
    plt.show()

# Visualizza i percorsi per alcuni cluster selezionati
for cluster_id in list(optimized_routes.keys())[:5]:
    cluster_data = coordinates[coordinates['Cluster'] == cluster_id].reset_index(drop=True)
    plot_optimized_route(cluster_id, cluster_data, optimized_routes[cluster_id])
