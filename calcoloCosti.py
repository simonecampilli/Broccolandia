import pandas as pd
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcola la distanza di Haversine in chilometri tra due punti geografici."""
    import math
    R = 6371  # Raggio terrestre in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2.0) ** 2
    c = 2 * math.atan2(np.sqrt(a), np.sqrt(1 - a))
    kilometers = R * c
    return kilometers


def create_distance_matrix_with_penalties(locations, penalties):
    """Crea una matrice delle distanze includendo le penalità per l'accessibilità."""
    size = len(locations)
    distance_matrix = {}
    for from_counter in range(size):
        distance_matrix[from_counter] = {}
        for to_counter in range(size):
            if from_counter == to_counter:
                distance_matrix[from_counter][to_counter] = 0
            else:
                lat1, lon1 = locations[from_counter]
                lat2, lon2 = locations[to_counter]
                dist = haversine_distance(lat1, lon1, lat2, lon2)
                # Applica la penalità se uno dei due contatori non è facilmente accessibile
                penalty = max(penalties[from_counter], penalties[to_counter])
                distance_matrix[from_counter][to_counter] = dist * penalty
    return distance_matrix


def solve_tsp(distance_matrix):
    """Risolvi il TSP utilizzando OR-Tools."""
    size = len(distance_matrix)
    manager = pywrapcp.RoutingIndexManager(size, 1, 0)  # 1 veicolo, partenza dal nodo 0
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Ritorna la distanza tra due nodi."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node] * 1000)  # Converti km in metri

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Imposta la strategia per la prima soluzione
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Risolvi il problema
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = solution.Value(routing.NextVar(index))
        # Aggiungi il nodo finale per completare il percorso
        route.append(manager.IndexToNode(index))
        return route
    else:
        return None


def main():
    # Fattore di penalità per i contatori non facilmente accessibili
    penalty_factor = 1.5

    # Leggi i dati dal file CSV
    df = pd.read_csv('preprocessed_data_updated.csv')

    # Assicurati che le colonne di data e ora siano nel formato corretto
    df['Data Lettura'] = pd.to_datetime(df['Data Lettura'])
    df['Ora Lettura'] = pd.to_datetime(df['Ora Lettura'], format='%H:%M:%S').dt.time

    # Mappa l'accessibilità a un fattore numerico di penalità
    # 'Sì' significa accessibile, 'No' significa non accessibile
    df['Accessibilità'] = df['Accessibilità'].map({'Sì': 1.0, 'No': penalty_factor})

    # Ottieni la lista dei letturisti
    meter_readers = df['Codice Letturista'].unique()

    # Processa ciascun letturista
    for letturista in meter_readers:
        df_letturista = df[df['Codice Letturista'] == letturista].reset_index(drop=True)
        locations = list(zip(df_letturista['Latitude'], df_letturista['Longitude']))
        penalties = df_letturista['Accessibilità'].tolist()

        # Crea la matrice delle distanze con le penalità
        distance_matrix = create_distance_matrix_with_penalties(locations, penalties)

        # Risolvi il TSP
        route = solve_tsp(distance_matrix)

        # Mappa gli indici del percorso ai dati originali
        if route:
            ordered_df = df_letturista.iloc[route].reset_index(drop=True)
            # Stampa o salva il percorso ottimizzato per questo letturista
            print(f"Percorso ottimizzato per il Letturista {letturista}:")
            print(ordered_df[['Latitude', 'Longitude', 'Accessibilità']])
        else:
            print(f"Nessuna soluzione trovata per il Letturista {letturista}")


if __name__ == '__main__':
    main()
