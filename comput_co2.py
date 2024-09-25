import pandas as pd
import geopy.distance

# 1. Leggi il file Excel
df = pd.read_excel('/Users/michelemenabeni/PycharmProjects/AQA/Report_Complessivo_AqA_blocco35_Apr.mag.24.xlsx')
print(df.columns)
df = df.dropna(subset=['Latitude', 'Longitude'])


# 2. Funzione per calcolare la distanza tra due coordinate
def calcola_distanza(coord1, coord2):
    return geopy.distance.geodesic(coord1, coord2).km


# 3. Filtra i dati per operatore e data e calcola la distanza tra i punti
def calcola_emissioni_per_operatore(df, fattore_emissione_g_km=120):
    emissioni_giornaliere = {}

    # Raggruppa i dati per operatore e data
    gruppi = df.groupby(['Codice Letturista', 'Data Lettura'])

    for (operatore, data), gruppo in gruppi:
        emissioni_totali = 0
        punti = gruppo[['Latitude', 'Longitude']].values
        distanza=0
        # Calcola la distanza tra contatori successivi e somma le emissioni
        for i in range(1, len(punti)):
            distanza_km = calcola_distanza(punti[i - 1], punti[i])
            emissioni_totali += distanza_km * fattore_emissione_g_km / 1000  # Emissioni in kg
            distanza+=distanza_km

        emissioni_giornaliere[(operatore, data)] = {'em':emissioni_totali,'dist':distanza}

    return emissioni_giornaliere


# 4. Esegui il calcolo delle emissioni
emissioni_per_operatore = calcola_emissioni_per_operatore(df)

# 5. Mostra i risultati per un operatore specifico
for (operatore, data), ris in emissioni_per_operatore.items():
    print(f"Operatore: {operatore}, Data: {data}, Emissioni di CO₂: {ris['em']:.2f} kg, Distanza: {ris['dist']:.2f}")
