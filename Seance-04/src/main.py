#coding:utf8

import numpy as np
import pandas as pd
import scipy 
import scipy.stats as stats

#https://docs.scipy.org/doc/scipy/reference/stats.html


dist_names = ['norm', 'beta', 'gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2', 'bradford', 'burr', 'burr12', 'cauchy', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponweib', 'exponpow', 'f', 'genpareto', 'gausshyper', 'gibrat', 'gompertz', 'gumbel_r', 'pareto', 'pearson3', 'powerlaw', 'triang', 'weibull_min', 'weibull_max', 'bernoulli', 'betabinom', 'betanbinom', 'binom', 'geom', 'hypergeom', 'logser', 'nbinom', 'poisson', 'poisson_binom', 'randint', 'zipf', 'zipfian']

print(dist_names)

# Étape 1 et 2 :

#les distributions statistiques de variables discrètes :

#La loi de Dirac
dirac = stats.rv_discrete(name="dirac", values=([0], [1]))
m, v = dirac.stats(moments="mv")
print("LOI DE DIRAC. Moyenne :", float(m), "| Écart-type :", float(np.sqrt(v)))

#La loi uniforme discrète
uniforme_discrete = stats.randint(low=0, high=10)
m, v = uniforme_discrete.stats(moments="mv")
print("LOI UNIFORME DISCRÈTE. Moyenne :", float(m), "| Écart-type :", float(np.sqrt(v)))

#La loi binomiale
binomiale = stats.binom(n=10, p=0.5)
m, v = binomiale.stats(moments="mv")
print("LOI BINOMIALE. Moyenne :", float(m), "| Écart-type :", float(np.sqrt(v)))

#La loi de Poisson
poisson = stats.poisson(mu=3)
m, v = poisson.stats(moments="mv")
print("LOI DE POISSON. Moyenne :", float(m), "| Écart-type :", float(np.sqrt(v)))

#La loi de Zipf-Mandelbrot
s, q, N = 1.2, 1.0, 30
k = np.arange(1, N + 1)
w = 1 / ((k + q) ** s)
zipf_mandelbrot = stats.rv_discrete(name="zipf_mandelbrot", values=(k, w / w.sum()))

m, v = zipf_mandelbrot.stats(moments="mv")
print("LOI ZIPF–MANDELBROT | Moyenne:", float(m), "| Écart-type:", float(np.sqrt(v)))

#les distributions statistiques de variables continues :

#La loi Exponentielle (de Poisson)
expo = stats.expon(scale=1/0.8)  # λ = 0.8
m, v = expo.stats(moments="mv")
print("LOI EXPONENTIELLE. Moyenne:", float(m), "| Écart-type:", float(np.sqrt(v)))

#La loi Normale
normale = stats.norm(loc=0, scale=1)
m, v = normale.stats(moments="mv")
print("LOI NORMALE. Moyenne:", float(m), "| Écart-type:", float(np.sqrt(v)))

#La loi Log-normale
lognormale = stats.lognorm(s=0.6, scale=np.exp(0))
m, v = lognormale.stats(moments="mv")
print("LOI LOG-NORMALE. Moyenne:", float(m), "| Écart-type:", float(np.sqrt(v)))

#La loi du X2
chi2 = stats.chi2(df=4)
m, v = chi2.stats(moments="mv")
print("LOI DU CHI². Moyenne:", float(m), "| Écart-type:", float(np.sqrt(v)))

#La loi de Pareto
pareto = stats.pareto(b=2.5, scale=1)
m, v = pareto.stats(moments="mv")
print("LOI DE PARETO. Moyenne:", float(m), "| Écart-type:", float(np.sqrt(v)))

#Visualisation des distributions :

import os
import matplotlib.pyplot as plt
os.makedirs("figures", exist_ok=True)

# Dirac
x = np.arange(-3, 4)
plt.figure()
plt.stem(x, dirac.pmf(x))
plt.title("Loi de Dirac (k₀=0)")
plt.xlabel("k"); plt.ylabel("P(X=k)")
plt.tight_layout()
plt.savefig("figures/dirac.png", dpi=150)
plt.close()

# Uniforme discrète 
x = np.arange(0, 10)
plt.figure()
plt.stem(x, uniforme_discrete.pmf(x))
plt.title("Loi uniforme discrète [0,9]")
plt.xlabel("k"); plt.ylabel("P(X=k)")
plt.tight_layout()
plt.savefig("figures/uniforme_discrete.png", dpi=150)
plt.close()

# Binomiale 
x = np.arange(0, 11)
plt.figure()
plt.stem(x, binomiale.pmf(x))
plt.title("Loi binomiale n=10, p=0.5")
plt.xlabel("k"); plt.ylabel("P(X=k)")
plt.tight_layout()
plt.savefig("figures/binomiale.png", dpi=150)
plt.close()

# Poisson 
x = np.arange(0, 16)
plt.figure()
plt.stem(x, poisson.pmf(x))
plt.title("Loi de Poisson λ=3")
plt.xlabel("k"); plt.ylabel("P(X=k)")
plt.tight_layout()
plt.savefig("figures/poisson.png", dpi=150)
plt.close()

# Zipf–Mandelbrot 
plt.figure()
plt.stem(k, zipf_mandelbrot.pmf(k))
plt.title("Loi de Zipf–Mandelbrot s=1.2, q=1, N=30")
plt.xlabel("k"); plt.ylabel("P(X=k)")
plt.tight_layout()
plt.savefig("figures/zipf_mandelbrot.png", dpi=150)
plt.close()

# Exponentielle (processus de Poisson)
x = np.linspace(0, 10, 500)
plt.figure()
plt.plot(x, expo.pdf(x))
plt.title("Loi exponentielle (λ=0.8)")
plt.xlabel("x"); plt.ylabel("f(x)")
plt.tight_layout()
plt.savefig("figures/exponentielle.png", dpi=150)
plt.close()

# Normale
x = np.linspace(-5, 5, 500)
plt.figure()
plt.plot(x, normale.pdf(x))
plt.title("Loi normale μ=0, σ=1")
plt.xlabel("x"); plt.ylabel("f(x)")
plt.tight_layout()
plt.savefig("figures/normale.png", dpi=150)
plt.close()

# Log-normale
x = np.linspace(1e-3, 10, 500)
plt.figure()
plt.plot(x, lognormale.pdf(x))
plt.title("Loi log-normale μ=0, σ=0.6")
plt.xlabel("x"); plt.ylabel("f(x)")
plt.tight_layout()
plt.savefig("figures/lognormale.png", dpi=150)
plt.close()

# Chi² (ddl=4)
x = np.linspace(0, 25, 500)
plt.figure()
plt.plot(x, chi2.pdf(x))
plt.title("Loi du χ² (ddl=4)")
plt.xlabel("x"); plt.ylabel("f(x)")
plt.tight_layout()
plt.savefig("figures/chi2.png", dpi=150)
plt.close()

# Pareto (α=2.5, x_m=1)
x = np.linspace(0.1, 10, 500)
plt.figure()
plt.plot(x, pareto.pdf(x))
plt.title("Loi de Pareto α=2.5, xₘ=1")
plt.xlabel("x"); plt.ylabel("f(x)")
plt.tight_layout()
plt.savefig("figures/pareto.png", dpi=150)
plt.close()

print("Toutes les figures ont été enregistrées dans le dossier 'figures/'")