import numpy as np
import matplotlib.pyplot as plt
import fileinput
from math import exp 
from scipy import optimize
from scipy import odr


#On charge les données de l'aimantation et la hauteur de l'aimant permanent dans un tableau dans un tableau
l=np.loadtxt('Data/AimantPermanent.txt')
l[:,0]*=1e-9

#On défini la dérivée de B par rapport a z, avec les paramètres déterminé par le callibrage du champ B en fonction de la position précédemment déterminé
def dBz(z):
    B0=56.190
    z1=-0.59179
    z2=-0.58146
    R=1.4938
    return B0*R*R*(1/pow((pow(z-z1,2)+pow(R,2)),1.5)-1/pow((pow(z-z2,2)+pow(R,2)),1.5))

#On défini la même dérivée avec de précédents paramètres pour corriger l'erreur faite sur l'acquisition 
def dBz2(z):
    B0=40720
    z1=-0.59376
    z2=-0.57951
    R=1.4938
    return B0*R*R*(1/pow((pow(z-z1,2)+pow(R,2)),1.5)-1/pow((pow(z-z2,2)+pow(R,2)),1.5))

#On corrige grace aux 2 fonctions précédemment définies l'aimantation obtenues (on remplace dans l'aimantation la valeur précédente de dBz par la nouvelle, et on ajuste les valeurs d'un facteur 10² pour les obtenirs en unités S.I)
for i in range(len(l)):
    l[i,0]*=1e-2*dBz2(l[i,1])/dBz(l[i,1])

#On crée une fonction sous forme de polynome afin de fitter les points de l'aimantation en fonction de l'aimant permanent
def fitfunc(z,a,b,c,d,e,f,g):
    return a + b*z + c*z*z + d*z*z*z + e*z*z*z*z + f*z*z*z*z*z + g*pow(z,0.5)

#On détermine la valeurs des paramètres grace a la fonction optimize.curve_fit
p0=(1,1,1,1,1,1,1)
p, cv = optimize.curve_fit(fitfunc,l[:,1],l[:,0],p0)
print(p)

#Enfin, on affiche les points corrigés ainsi que le fit réalisé
plt.figure(figsize=(16,14))
plt.errorbar(l[:,1],l[:,0],fmt='+',yerr=2e-2*l[:,0])
plt.plot(l[:,1],fitfunc(l[:,1],p[0],p[1],p[2],p[3],p[4],p[5],p[6]),label='fit')
plt.title('Aimantation en fonction de la hauteur')
plt.xlabel('hauteur (cm)')
plt.ylabel('Aimantation (A/m)')
plt.legend()
plt.show()

#On inscrit les paramètres du fit dans un fichier pour utilisation dans un autre programme
f = open('Data/Modele_A.txt','w')
f.write(f'{p[0]} {p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}')
f.close()