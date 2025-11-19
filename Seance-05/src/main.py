#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats

#C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement que pratiquement. D'autre, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les résultats ne sont pas conformes à la théorie probabiliste.
#Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
#Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

#Par convention, on place les fonctions locales au début du code après les bibliothèques.
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Théorie de l'échantillonnage (intervalles de fluctuation)
#L'échantillonnage se base sur la répétitivité.
print("Résultat sur le calcul d'un intervalle de fluctuation")

donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

#Moyennes arrondies
moyennes = donnees.mean()
moyennes_arrondies = pd.Series({
    col: round(moyennes[col])
    for col in moyennes.index
})
print("Moyennes arrondies :")
print(moyennes_arrondies)

#Somme moyennes
somme_moyennes = moyennes_arrondies.sum()
freq_echantillon = moyennes_arrondies.apply(lambda x: round(x / somme_moyennes, 2))
print("Fréquences de l'échantillon moyen :")
print(freq_echantillon)

#Population mère
population_mere = pd.Series({
    "Pour": 852,
    "Contre": 911,
    "Sans opinion": 422
})
somme_pop = population_mere.sum()
freq_population = population_mere.apply(lambda x: round(x / somme_pop, 2))
print("Fréquences de la population mère :")
print(freq_population)

#Intervalle de fluctuation à 95%
z = 1.96
n = somme_moyennes
print("Intervalle de fluctuation à 95 % :")
for opinion, f in freq_echantillon.items():
    marge = z * math.sqrt(f * (1 - f) / n)
    borne_inf = round(f - marge, 3)
    borne_sup = round(f + marge, 3)
    print(f"{opinion} : [{borne_inf} ; {borne_sup}]")

#Théorie de l'estimation (intervalles de confiance)
#L'estimation se base sur l'effectif.
print("Résultat sur le calcul d'un intervalle de confiance")

ech1 = donnees.iloc[0]
ech1_list = list(ech1)
total1 = sum(ech1_list)
freq1 = [round(x / total1, 3) for x in ech1_list]

print("Premier échantillon (liste) :", ech1_list)
print("Effectif total :", total1)
print("Fréquences du premier échantillon :", freq1)

#Intervalle de fluctuation à 95%
z = 1.96
print("\nIntervalle de confiance à 95 % pour chaque opinion :")
for f in freq1:
    marge = z * math.sqrt(f * (1 - f) / total1)
    borne_inf = round(f - marge, 3)
    borne_sup = round(f + marge, 3)
    print(f"{f} : [{borne_inf} ; {borne_sup}]")

#Théorie de la décision (tests d'hypothèse)
#La décision se base sur la notion de risques alpha et bêta.
#Comme à la séance précédente, l'ensemble des tests se trouve au lien : https://docs.scipy.org/doc/scipy/reference/stats.html
print("Théorie de la décision")

test1 = ouvrirUnFichier("./data/Loi-normale-Test-1.csv")
test2 = ouvrirUnFichier("./data/Loi-normale-Test-2.csv")
col1 = test1.iloc[:, 0]
col2 = test2.iloc[:, 0]

stat1, p1 = scipy.stats.shapiro(col1)
stat2, p2 = scipy.stats.shapiro(col2)

print("Test 1 : p-value =", p1)
print("Test 2 : p-value =", p2)

if p1 > 0.05:
    print("→ Le fichier 1 suit une distribution normale.")
else:
    print("→ Le fichier 1 ne suit pas une distribution normale.")

if p2 > 0.05:
    print("→ Le fichier 2 suit une distribution normale.")
else:
    print("→ Le fichier 2 ne suit pas une distribution normale.")