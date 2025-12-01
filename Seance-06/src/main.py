#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import math

#Fonction pour ouvrir les fichiers
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Fonction pour convertir les données en données logarithmiques
def conversionLog(liste):
    log = []
    for element in liste:
        log.append(math.log(element))
    return log

#Fonction pour trier par ordre décroissant les listes (îles et populations)
def ordreDecroissant(liste):
    liste.sort(reverse = True)
    return liste

#Fonction pour obtenir le classement des listes spécifiques aux populations
def ordrePopulation(pop, etat):
    ordrepop = []
    for element in range(0, len(pop)):
        if np.isnan(pop[element]) == False:
            ordrepop.append([float(pop[element]), etat[element]])
    ordrepop = ordreDecroissant(ordrepop)
    for element in range(0, len(ordrepop)):
        ordrepop[element] = [element + 1, ordrepop[element][1]]
    return ordrepop

#Fonction pour obtenir l'ordre défini entre deux classements (listes spécifiques aux populations)
def classementPays(ordre1, ordre2):
    classement = []
    if len(ordre1) <= len(ordre2):
        for element1 in range(0, len(ordre2) - 1):
            for element2 in range(0, len(ordre1) - 1):
                if ordre2[element1][1] == ordre1[element2][1]:
                    classement.append([ordre1[element2][0], ordre2[element1][0], ordre1[element2][1]])
    else:
        for element1 in range(0, len(ordre1) - 1):
            for element2 in range(0, len(ordre2) - 1):
                if ordre2[element2][1] == ordre1[element1][1]:
                    classement.append([ordre1[element1][0], ordre2[element2][0], ordre1[element][1]])
    return classement

#Partie BONUS :
def analyseRangs(rang1, rang2):
    rho, _ = scipy.stats.spearmanr(rang1, rang2)
    tau, _ = scipy.stats.kendalltau(rang1, rang2)
    return rho, tau

#Partie sur les îles
df_iles = ouvrirUnFichier("./data/island-index.csv")
iles = pd.DataFrame(ouvrirUnFichier("./data/island-index.csv"))

# Extraction en list() comme demandé par la séance
surface = df_iles["Surface (km²)"].astype(float).tolist()
cote = df_iles["Trait de côte (km)"].astype(float).tolist()

# Ajout des surfaces continentales (sans unité)
surface.extend([
    85545323.0,
    37856841.0,
    7768030.0,
    7605049.0
])

# Classement décroissant et conversion en rangs
surface_sorted = ordreDecroissant(surface)
rangs = list(range(1, len(surface_sorted) + 1))

# Visualisation loi rang–taille linéaire
plt.figure(figsize=(8,6))
plt.plot(rangs, surface_sorted)
plt.title("Loi rang–taille – Îles et continents")
plt.xlabel("Rang")
plt.ylabel("Surface (km²)")
plt.tight_layout()
plt.savefig("figures/iles_lineaire.png")
plt.close()

# Visualisation log–log rang–taille
log_surface = conversionLog(surface_sorted)
log_rangs = conversionLog(rangs)

plt.figure(figsize=(8,6))
plt.plot(log_rangs, log_surface)
plt.title("Loi rang–taille (log-log) – Îles")
plt.xlabel("log(rang)")
plt.ylabel("log(surface)")
plt.tight_layout()
plt.savefig("figures/iles_loglog.png")
plt.close()

# Oui, il est possible de tester les rangs
# via les coefficients de Spearman et Kendall.




# Analyse des rangs Surface vs Côte
# Générer les vectors de rangs NUMÉRIQUES pour surface et côte
def genererRangs(liste):
    pairs = list(zip(liste, range(len(liste))))
    pairs.sort(key=lambda x: x[0], reverse=True)
    return [i + 1 for _, i in pairs]

rang_surface = genererRangs(surface)
rang_cote = genererRangs(cote)

# Vérifier et égaliser les dimensions si besoin
n = min(len(rang_surface), len(rang_cote))
rang_surface = rang_surface[:n]
rang_cote = rang_cote[:n]

rho, tau = analyseRangs(rang_surface, rang_cote)
print("BONUS Îles — Surface vs Côte → Spearman =", rho, ", Kendall =", tau)

#Attention ! Il va falloir utiliser des fonctions natives de Python dans les fonctions locales que je vous propose pour faire l'exercice. Vous devez caster l'objet Pandas en list().






#Partie sur les populations des États du monde
#Source. Depuis 2007, tous les ans jusque 2025, M. Forriez a relevé l'intégralité du nombre d'habitants dans chaque États du monde proposé par un numéro hors-série du monde intitulé États du monde. Vous avez l'évolution de la population et de la densité par année.
df_monde = ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv")
monde = pd.DataFrame(df_monde)

etat_m = monde["État"].astype(str).tolist()
pop2007_m = monde["Pop 2007"].astype(float).tolist()
pop2025_m = monde["Pop 2025"].astype(float).tolist()
dens2007_m = monde["Densité 2007"].astype(float).tolist()
dens2025_m = monde["Densité 2025"].astype(float).tolist()

# Préparer les colonnes population/densité
surfaces_corr = []
densites_corr = []
etats = monde["État"].astype(str).tolist()
pop_corr = []

for an in range(2007, 2026):
    c_pop = f"Pop {an}"
    c_den = f"Densité {an}"
    if c_pop in monde.columns and c_den in monde.columns:

        pop = monde[c_pop].astype(float).tolist()
        dens = monde[c_den].astype(float).tolist()

        ordre_pop = ordrePopulation(pop, etats)
        ordre_dens = ordrePopulation(dens, etats)

        if len(ordre_pop) > 0 and len(ordre_dens) > 0:
            rangs_pop = [x[0] for x in ordre_pop]
            rangs_den = [x[0] for x in ordre_dens]

            rho, tau = analyseRangs(rangs_pop, rangs_den)
            surfaces_corr.append([an, rho, tau])

            print(f"Année {an} : Spearman =", rho, ", Kendall =", tau)

# Export du bonus 2007–2025
pd.DataFrame(surfaces_corr, columns=["Année", "Spearman", "Kendall"]) \
  .to_csv("figures/corr_rangs_2007_2025.csv", index=False)

print("Bonus rangs 2007–2025 terminé : Figures et CSV dans /figures/")

#Attention ! Il va falloir utiliser des fonctions natives de Python dans les fonctions locales que je vous propose pour faire l'exercice. Vous devez caster l'objet Pandas en list().


