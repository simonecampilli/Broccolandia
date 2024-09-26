import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial import distance_matrix
import numpy as np
import matplotlib.pyplot as plt

# Carica i dati
data_path = 'Report_Complessivo_AqA_blocco35_Apr.mag.24.xlsx'  # Modifica con il percorso del tuo file
data = pd.read_excel(data_path, sheet_name='Letture')
coordinates = data[['Latitude', 'Longitude']].dropna().drop_duplicates()

# Applicazione di K-means per la formazione di 50 cluster
kmeans = KMeans(n_clusters=50, random_state=0).fit(coordinates)
coordinates['Cluster'] = kmeans.labels_

# Definizione della funzione 2-opt
def two_opt(route, dist_matrix):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 2, len(route)):
                if j - i == 1: continue  # Salta gli scambi di nodi adiacenti
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1]  # Scambio e inversione
                if np.sum(dist_matrix[np.arange(len(new_route)), new_route]) < np.sum(dist_matrix[np.arange(len(best)), best]):
                    best = new_route
                    improved = True
        route = best
    return best

# Ottimizzazione dei percorsi per ciascun cluster
optimized_routes = {}
for cluster_id in range(50):
    cluster_points = coordinates[coordinates['Cluster'] == cluster_id][['Latitude', 'Longitude']].to_numpy()
    if len(cluster_points) > 1:
        dist_matrix_cluster = distance_matrix(cluster_points, cluster_points)
        initial_route_cluster = np.arange(len(cluster_points))
        optimized_route = two_opt(initial_route_cluster, dist_matrix_cluster)
        optimized_routes[cluster_id] = optimized_route

# Funzione per visualizzare il percorso ottimizzato per un cluster
def plot_optimized_route(cluster_id, coordinates, optimized_route):
    plt.figure(figsize=(10, 8))
    optimized_points = coordinates.iloc[optimized_route]
    plt.plot(optimized_points['Longitude'], optimized_points['Latitude'], 'o-', label=f'Cluster {cluster_id}')
    plt.title(f'Percorso ottimizzato per il Cluster {cluster_id}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.legend()
    plt.show()

# Visualizza i percorsi per i primi due cluster ottimizzati
for cluster_id in list(optimized_routes.keys())[:2]:
    cluster_data = coordinates[coordinates['Cluster'] == cluster_id]
    plot_optimized_route(cluster_id, cluster_data, optimized_routes[cluster_id])
