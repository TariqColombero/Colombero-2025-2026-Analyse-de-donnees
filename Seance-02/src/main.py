#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv","r") as fichier:
    contenu = pd.read_csv(fichier)

#5 Afficher le contenu du tableau.
print(contenu)      

#6 Calculer le nombre de lignes et de colonnes.
print("Nombre de lignes :", len(contenu))
print("Nombre de colonnes :", len(contenu.columns))

#7 Liste sur le type de chaque colonne.
print(contenu.dtypes)

#8 Liste sur le type de chaque colonne.
print("Aperçu du tableau :")
print(contenu.head)

#9 Selectionner la colonne "Inscrits".
print("Nombre des inscrits par départements :")
print(contenu.Inscrits)

#10 Calculer les effectifs de chaque colonnes.
# Créer une liste vide.
somme_colonnes = []

# Parcourir chaque colonne.
for col in contenu.columns:
    if contenu[col].dtype in ["int64", "float64"]:   # garder uniquement les colonnes numériques int et float.
        total = contenu[col].sum()
        somme_colonnes.append((col, total))

# Afficher le résultat
print("Sommes des colonnes aux valeurs quantitatives :")
for col, total in somme_colonnes:
    print(f"- {col} : {total}")

#11 Créer un diagramme en barres pour les colonnes à l'aide de matplotlib.

# Créer le dossier "images", s'il n'existe pas déjà.
import os 
os.makedirs("images", exist_ok=True) 

# Définir les colonnes à tracer
colonnes = ["Inscrits", "Votants"]

# Boucle sur chaque colonne
for col in colonnes:
    plt.figure(figsize=(16,10))
    
    # Tracer le diagramme en barres
    plt.bar(contenu["Libellé du département"], contenu[col], color="skyblue")
    
    # Mise en forme
    plt.xticks(rotation=90)
    plt.title(f"Nombre de {col} par département")
    plt.ylabel("Nombre d'électeurs")
    plt.xlabel("Départements")
    
    # Sauvegarde en PNG
    plt.tight_layout()
    plt.savefig(f"images/{col}.png", dpi=300)
    plt.close()

print("Diagrammes 'Inscrits.png' et 'Votants.png' enregistrés dans le dossier 'images'")

#12 Créer un diagramme circulaire à l'aide de matplotlib.
# Désactivé pour permettre l'exécution du code suivant

# Crée le dossier images_pie dans ce répertoire
#os.makedirs("./images_pie", exist_ok=True)

# Définir les colonnes à tracer
#colonnes = ["Abstentions", "Blancs", "Nuls", "Exprimés"]

# Boucle sur chaque département
#for idx, row in contenu.iterrows():
    # Données du département courant
    #valeurs = [row["Abstentions"], row["Blancs"], row["Nuls"], row["Exprimés"]]
    #labels = colonnes
    
    # Création de la figure
    #plt.figure(figsize=(6,6))
    #plt.pie(valeurs, labels=labels, autopct='%1.1f%%', startangle=90)
    
    # Titre avec le nom du département
    #plt.title(f"Répartition des votes - {row['Libellé du département']}", fontsize=12, fontweight="bold")
    
    # Sauvegarde de l'image
    #plt.savefig(f"images_pie/{row['Code du département']}_{row['Libellé du département']}.png", dpi=300)
    #plt.close()

#print("Diagrammes circulaires enregistrés dans le dossier 'images_pie'")

#13 Créer un histogramme de la colonne "Inscrits".

# Créer le dossier pour stocker l’histogramme
os.makedirs("images_hist", exist_ok=True)

# Histogramme de la distribution des inscrits
plt.figure(figsize=(10,6))
plt.hist(contenu["Inscrits"], bins=20, color="skyblue", edgecolor="black", density=True)

# Mise en forme
plt.title("Histogramme de la distribution des inscrits")
plt.xlabel("Nombre d'inscrits par département")
plt.ylabel("Densité (aire totale = 1)")

# Sauvegarde
plt.tight_layout()
plt.savefig("images_hist/histogramme_inscrits.png", dpi=300)
plt.close()

print("Histogramme 'histogramme_inscrits.png' enregistré dans le dossier 'images'")

#14 BONUS : Diagrammes circulaires des voix par candidat

# Créer un dossier pour stocker les diagrammes circulaires par candidat
os.makedirs("images_voix", exist_ok=True)

# On identifie les colonnes de voix (Voix, Voix.1, Voix.2, ...)
colonnes_voix = [col for col in contenu.columns if "Voix" in col]

# --- 1. Diagramme circulaire par département ---
#for index, row in contenu.iterrows():
    #voix = row[colonnes_voix]  # valeurs des voix

    # Récupérer les noms + prénoms des candidats correspondants
    #labels = []
    #for col in colonnes_voix:
        # Extraire l'indice (ex: "Voix.3" -> "3")
       # if "." in col:
        # indice = col.split(".")[1]
          #  nom = row[f"Nom.{indice}"]
          #  prenom = row[f"Prénom.{indice}"]
       # else:
           # nom = row["Nom"]
           # prenom = row["Prénom"]
        #labels.append(f"{prenom} {nom}")

    # Création du pie chart
   # plt.figure(figsize=(8, 8))
   # plt.pie(voix, labels=labels, autopct="%1.1f%%", startangle=90)

    # Titre
   #plt.title(f"Répartition des voix par candidat - {row['Libellé du département']}")

    # Sauvegarde (remplace espaces par _ dans le nom du fichier)
    #nom_fichier = row["Libellé du département"].replace(" ", "_")
    #plt.savefig(f"images_voix/{row['Code du département']}_{nom_fichier}.png", dpi=300)
    #plt.close()

# --- 2. Diagramme circulaire pour la France entière ---
voix_france = contenu[colonnes_voix].sum()

# Construire les labels des candidats à partir de la première ligne (valable pour tout le fichier)
labels_france = []
first_row = contenu.iloc[0]
for col in colonnes_voix:
    if "." in col:
        indice = col.split(".")[1]
        nom = first_row[f"Nom.{indice}"]
        prenom = first_row[f"Prénom.{indice}"]
    else:
        nom = first_row["Nom"]
        prenom = first_row["Prénom"]
    labels_france.append(f"{prenom} {nom}")

plt.figure(figsize=(8, 8))
plt.pie(voix_france, labels=labels_france, autopct="%1.1f%%", startangle=90)
plt.title("Répartition des voix par candidat - France entière")
plt.savefig("images_voix/France.png", dpi=300)
plt.close()

print("Diagrammes circulaires avec noms des candidats générés dans 'images_voix'")

