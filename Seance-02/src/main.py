# coding:utf-8
import os, re
import pandas as pd
import matplotlib.pyplot as plt

# 1. Charger les données
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv", "r") as f:
    contenu = pd.read_csv(f)

# 5. fficher le contenu du tableau
print(contenu)

# 6. Calculer le nombre de lignes et de colonnes
print("Nombre de lignes :", len(contenu))
print("Nombre de colonnes :", len(contenu.columns))

#7 Liste sur le type de chaque colonne
print(contenu.dtypes)

#8 Liste sur le type de chaque colonne
print("Aperçu du tableau:")
print(contenu.head)

#9 Sélectionner la colonne "Inscrits"
print("Nombre des inscrits par départements :")
print(contenu.Inscrits)

#10 Calculer les effectifs de chaque colonnes
print("\nNombre des inscrits par département :")
print(contenu["Inscrits"])
print("\nSommes colonnes numériques :\n", contenu.select_dtypes(include=["int64","float64"]).sum())

# 11. Diagrammes en barres : inscrits & votants
os.makedirs("images", exist_ok=True)
for c in ["Inscrits", "Votants"]:
    plt.figure(figsize=(12,6))
    plt.bar(contenu["Libellé du département"], contenu[c], color="cornflowerblue")
    plt.xticks(rotation=90)
    plt.title(f"Nombre de {c} par département")
    plt.ylabel("Nombre d’électeurs")
    plt.tight_layout()
    plt.savefig(f"images/{c}.png", dpi=300)
    plt.close()
print("→ Diagrammes 'Inscrits.png' et 'Votants.png' enregistrés")

# 12. Diagrammes circulaires : blancs, nuls, exprimés, abstentions
os.makedirs("images_pie", exist_ok=True)
cols_pie = ["Blancs", "Nuls", "Exprimés", "Abstentions"]
for _, row in contenu.iterrows():
    dep = re.sub(r"[^\w\-]", "_", row["Libellé du département"])
    plt.figure(figsize=(5,5))
    plt.pie([row[c] for c in cols_pie], labels=cols_pie, autopct="%1.1f%%", startangle=90)
    plt.title(f"Répartition des votes – {row['Libellé du département']}")
    plt.tight_layout()
    plt.savefig(f"images_pie/{row['Code du département']}_{dep}.png", dpi=300)
    plt.close()
print("→ Diagrammes circulaires enregistrés dans /images_pie")

# 13. Histogramme de la distribution des inscrits
os.makedirs("images_hist", exist_ok=True)
plt.figure(figsize=(10,6))
plt.hist(contenu["Inscrits"], bins=20, color="seagreen", edgecolor="black", density=True)
plt.title("Distribution des inscrits")
plt.xlabel("Nombre d’inscrits")
plt.ylabel("Densité")
plt.tight_layout()
plt.savefig("images_hist/histogramme_inscrits.png", dpi=300)
plt.close()
print("→ Histogramme enregistré dans /images_hist")

# 14. BONUS : diagrammes circulaires des voix par candidat
os.makedirs("images_voix", exist_ok=True)
vcols = [c for c in contenu.columns if c.startswith("Voix")]
def noms(r): return [r.get(f'Prénom.{i}', r['Prénom']) + " " + r.get(f'Nom.{i}', r['Nom']) for i in range(len(vcols))]
for _, r in contenu.iterrows():
    dep = re.sub(r"[^\w\-]", "_", r["Libellé du département"])
    plt.pie(r[vcols], labels=noms(r), autopct='%1.1f%%', startangle=90)
    plt.title(r['Libellé du département'])
    plt.savefig(f"images_voix/{r['Code du département']}_{dep}.png", dpi=300)
    plt.close()
plt.pie(contenu[vcols].sum(), labels=noms(contenu.iloc[0]), autopct='%1.1f%%', startangle=90)
plt.title("France entière")
plt.savefig("images_voix/France.png", dpi=300)
plt.close()
print("→ Diagrammes voix par candidat enregistrés (départements + France)")
