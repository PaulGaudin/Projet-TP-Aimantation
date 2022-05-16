import numpy as np
import matplotlib.pyplot as plt
import fileinput
from math import exp 
from scipy import optimize
from scipy import odr


#Récupération de la température en fonction de R(T)/R(0°C)
l=np.loadtxt('Data/EtalonnageH.txt')

#Creation et paramétrisation de la fonction de fit
def fitfunc(T,a,b,c):
    return a*T*T+b*T+c

p0=(1,1,1)
p, cv = optimize.curve_fit(fitfunc,l[:,0],l[:,2],p0)
print(f'Paramètres du modèle : {p}')

plt.figure(figsize=(16,14))

#Calcul de R(0°C) a partir de 2 points fixes
R01=fitfunc(27.5+273.15,p[0],p[1],p[2])
R01=111.4/R01

R02=fitfunc(77,p[0],p[1],p[2])
R02=22.4/R02

#Creation du fonction de poids prenant en compte les 2 modèles (réalisé a partir des 2 points fixes) avec un poids dépendant de la distance a leur point fixe
def finalfunc(func,x,p):

    return R01*func(x,p[0],p[1],p[2])*(x-77)/(300-77)+R02*func(x,p[0],p[1],p[2])*(1-(x-77)/(300-77))

#Affichage des 2 modèles et de la fonction de poids
plt.plot(R01*fitfunc(l[:,0],p[0],p[1],p[2]),l[:,0],label='Point Fixe : T=27.5°C')
plt.plot(R02*fitfunc(l[:,0],p[0],p[1],p[2]),l[:,0],label='Point Fixe : T=77K')
plt.plot(finalfunc(fitfunc,l[:,0],p),l[:,0],label='Modèle')
#plt.errorbar(finalfunc(fitfunc,l[:,0],p),l[:,0],fmt='+')
plt.legend()
print(f'R(0°C) pour le point T = 27°C, R = 111.4 Ohms : {R01} Ohms\nR(0°C) pour le point T = 77 K, R = 22.4 Ohms : {R02} Ohms')
plt.show()

#A ce stade, on possède un modèle de R(T), étant donné que nous voulons un modèle de T(R), on rééffectue un fit du modèle affiché précédemment, c'est a dire avec R(T) en x et T en y
A=finalfunc(fitfunc,l[:,0],p)

p0=(1,1,1)
p, cv = optimize.curve_fit(fitfunc,A,l[:,0],p0)

#Enfin, on écrit les paramètre de notre modèle final de T(R) dans un fichier pour une utilisation dans d'autre programmes.
f = open('Data/Modele_T.txt','w')
f.write(f'{p[0]} {p[1]} {p[2]}')
f.close()