import networkx as nx
import matplotlib.pyplot as plt
import random

# Paramètres
n1 = 40  # taille groupe 1
n2 = 40  # taille groupe 2
p_intra = 0.3  # probabilité de lien à l'intérieur de chaque groupe
p_inter = 0.01  # probabilité de lien entre les groupes (faible = polarisation)

G = nx.Graph()

# Ajouter les nœuds avec un attribut "group"
group1 = range(n1)
group2 = range(n1, n1 + n2)

G.add_nodes_from(group1, group=1)
G.add_nodes_from(group2, group=2)

# Ajouter les arêtes intra-groupe
for i in group1:
    for j in group1:
        if i < j and random.random() < p_intra:
            G.add_edge(i, j)

for i in group2:
    for j in group2:
        if i < j and random.random() < p_intra:
            G.add_edge(i, j)

# Ajouter quelques arêtes inter-groupes
for i in group1:
    for j in group2:
        if random.random() < p_inter:
            G.add_edge(i, j)

# Positionnement : layout force dirigée
pos = nx.spring_layout(G, k=0.3, iterations=100)

# Couleurs : un groupe = une couleur
colors = ["tab:blue" if G.nodes[n]["group"] == 1 else "tab:orange" for n in G.nodes()]

plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=80)
nx.draw_networkx_edges(G, pos, alpha=0.4, width=0.8)
plt.axis("off")
plt.title("Schéma de type Polarized Crowds")
plt.tight_layout()
plt.show()

plt.savefig("polarized_crowds_schema.png", dpi=300)