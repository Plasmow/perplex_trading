from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from influences import *

# --- 1. Définir les agents ---
class Trader(Agent):    
    def __init__(self, unique_id, model, profile, herding_prob, leverage):
        super().__init__(unique_id, model)
        self.profile = profile
        self.herding_prob = herding_prob  # Probabilité de mimétisme
        self.leverage = leverage  # Niveau de levier
        self.position = "NEUTRAL"  # "BUY", "SELL", ou "NEUTRAL"
        self.liquidated = False  # Indique si l'agent est liquidé

    def step(self):
        # Si liquidé, aucune action
        if self.liquidated:
            return

        # 1. Mimétisme (en fonction des voisins)
        neighbors = self.model.grid.get_neighbors(self.unique_id, include_center=False)
        neighbor_positions = [self.model.schedule.agents[n].position for n in neighbors]
        dominant_action = max(set(neighbor_positions), key=neighbor_positions.count) if neighbor_positions else "NEUTRAL"

        if random.random() < self.herding_prob and dominant_action != "NEUTRAL":
            self.position = dominant_action

        # 2. Règles spécifiques au profil
        if self.profile == "Market Maker":
            self.market_maker_logic()
        elif self.profile == "Degen":
            self.degen_logic()
        elif self.profile == "Swing Trader":
            self.swing_trader_logic()

        # 3. Vérifier liquidation forcée
        if random.random() < self.leverage:  # Simuler un mouvement du marché contre eux
            self.position = "SELL"
            self.liquidated = True  # Liquidation forcée déclenchée

    def market_maker_logic(self):
        """Market Makers annulent fréquemment et repostent des ordres."""
        if random.random() < 0.5:  # 50% chance de changer d'ordre
            self.position = "BUY" if random.random() < 0.5 else "SELL"

    def degen_logic(self):
        """Degens utilisent un effet de levier élevé et paniquent facilement."""
        if self.position == "SELL" and random.random() < 0.8:  # Forte probabilité de paniquer
            self.liquidated = True

    def swing_trader_logic(self):
        """Swing Traders placent peu d'ordres, mais suivent les signaux macro."""
        if random.random() < 0.2:  # Réagit lentement
            self.position = "BUY" if random.random() < 0.5 else "SELL"

# --- 2. Définir le modèle ---
class CryptoMarketModel(Model):
    def __init__(self, num_agents, graph):
        self.num_agents = num_agents
        self.schedule = SimultaneousActivation(self)
        self.grid = NetworkGrid(graph)
        self.running = True

        # Créer les agents
        profiles = ["Market Maker", "Degen", "Swing Trader"]
        for i, node in enumerate(graph.nodes):
            profile = random.choice(profiles)
            herding_prob = random.uniform(0.1, 0.9)
            leverage = random.uniform(0.2, 0.8) if profile == "Degen" else 0.1
            agent = Trader(i, self, profile, herding_prob, leverage)
            self.schedule.add(agent)
            self.grid.place_agent(agent, node)

    def step(self):
        self.schedule.step()


if __name__ == "__main__":
    filepath = "orders.csv"  # Remplacez par le chemin de votre fichier

    # Étape 1 : Chargement et nettoyage des données
    df_clean = load_and_clean_data(filepath)
    
    # Étape 2 : Détection des liens d'influence
    influence_links = detect_influence_links(df_clean)

    actions_simultanees = influence_links.T @ influence_links

    G = graphe(actions_simultanees)
    model = CryptoMarketModel(num_agents=12, graph=G)

    order_book = {"OrderHash" : [],
                  "Block" : [],
                  "Action" : [],
                  "Price" : [],
                  "Quantity" : [],
                  "OrderType" :[],
                  "Subaccount" : []}

    for i in range(10):  # Simulate 10 steps
        print(f"Step {i+1}")
        model.step()

        # Track and print positions after each step
        for agent in model.schedule.agents :
            if agent.position != "NEUTRAL" :
                hash_id_decimal = random.randint(0,1000000000)
                hash_id = hex(hash_id_decimal)
                price = random.randint(1,1000000)
                quantity = random.randint(1, 10)

                order_book["OrderHash"].append(hash_id)
                order_book["Block"].append(i)
                order_book["Action"].append("EVENT_NEW")
                order_book["Price"].append(price)
                order_book["Quantity"].append(quantity)
                order_book["OrderType"].append(agent.position)
                order_book["Subaccount"].append(agent.unique_id)

    # Dessin du graphe avec labels pour les nœuds (SubaccountID) et une échelle de poids pour les arêtes
    pos = nx.circular_layout(G)  # Positionnement des nœuds avec le layout spring
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='skyblue', font_size=8, font_weight='bold', edge_color='gray')

    # Ajout des poids sur les arêtes (représentant l'intensité de l'influence)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    data = pd.DataFrame(order_book)
    data.to_csv("order_book.csv", index=False)

    # Affichage du graphe
    plt.title("Réseau d'interactions des Subaccounts")
    plt.show()
