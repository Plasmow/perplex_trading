import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import networkx as nx

# Initialisation du temps
start = time.time()

# Étape 1 : Chargement et nettoyage des données
def load_and_clean_data(filepath):
    # Lecture du fichier CSV
    file_path = "orders.csv"  # Remplace par le chemin réel de ton fichier
    columns = ["OrderHash", "Block", "Action", "Price", "Quantity", "OrderType", "SubaccountID"]
    df = pd.read_csv(file_path, names=columns, skiprows=1)

    return df


# Étape 2 : Identifier des liens d'influence
def detect_influence_links(df, time_window=60):
    # Liste pour stocker les liens d'influence
    influence_links = []

    # Trier les données par bloc et sous-compte
    df = df.sort_values(by=['Block', 'SubaccountID'])

    # On nomme les comptes avec leur numéro d'apparition
    accounts = {}
    numero = 0

    # Permet de connaître qui a agit sur le bloc courant
    actions_on_block = [0 for _ in range(df["SubaccountID"].nunique())]
    block_number = 0

    # Calculer les différences de blocs entre les actions
    for _, row in df.iterrows():

        # Si changement de block, on enregistre les acteurs du block dans la matrice
        if row['Block'] != block_number :
            block_number = row['Block']
            influence_links.append(actions_on_block)
            actions_on_block = [0 for _ in range(df["SubaccountID"].nunique())]

        # On nomme les comptes pas visités
        if row['SubaccountID'] not in accounts :
            accounts[row['SubaccountID']] = numero
            numero += 1
        
        # On enregistre l'acteur sur le block courant
        actions_on_block[accounts[row['SubaccountID']]] = 1

    # Retourner les liens d'influence détectés
    return np.array(influence_links)


def graphe(actions_simultanees) :

    # Étape 3.1 : Construction du réseau d'interactions
    # Graphique des influences
    G = nx.DiGraph()

    # Ajouter des nœuds pour chaque SubaccountID unique
    subaccounts = []
    for k in range(len(actions_simultanees)) :
        subaccounts.append(k)
    G.add_nodes_from(subaccounts)

    # On ajoute les arêtes d'influences avec leur poids entre les comptes
    for i in range(len(actions_simultanees)) :
        for j in range(len(actions_simultanees[0])) :
            if actions_simultanees[i][j] != 0 :
                G.add_edge(i, j, weight=actions_simultanees[i][j])

    return G


# Exemple d'exécution
if __name__ == "__main__":
    filepath = "orders.csv"  # Remplacez par le chemin de votre fichier

    # Étape 1 : Chargement et nettoyage des données
    df_clean = load_and_clean_data(filepath)
    
    # Étape 2 : Détection des liens d'influence
    influence_links = detect_influence_links(df_clean)


    actions_simultanees = influence_links.T @ influence_links


    graphe(actions_simultanees)
