import numpy as np
import matplotlib.pyplot as plt
import fileinput
from math import exp 
from scipy import optimize
from scipy import odr

#Chargement des données
l=np.loadtxt('Data/GadSulfOctH.txt')
l[:,0]*=1e-9

#Creation d'un fit par une loi affine, et ajustement des points par la courbe de l'aimant permanent (Cf Compte rendu)
def fitfunc(z,b,a):
    return a+b*z

p2=np.loadtxt(f'Data/Modele_A.txt')

def fitfunc2(z,a,b,c,d,e,f,g):
    return a + b*z + c*z*z + d*z*z*z + e*z*z*z*z + f*z*z*z*z*z + g*pow(z,0.5)

def finalfunc(z,p,p2):
    return 1e5*fitfunc(z,p[0],p[1])/fitfunc2(z,p2[0],p2[1],p2[2],p2[3],p2[4],p2[5],p2[6])

p0=(1,1)
p, cv = optimize.curve_fit(fitfunc,l[:,3],l[:,2],p0)
print(f"Chi = {p[0]}")

p0=(1,1)
p3, cv = optimize.curve_fit(fitfunc,l[:,3],l[:,2]*1e5/fitfunc2(l[:,3],p2[0],p2[1],p2[2],p2[3],p2[4],p2[5],p2[6]),p0,maxfev=10000)
print(f"Chi corrigé = {p3[0]}")


#Affichage des données et du plot pour vérification de la qualité de ce dernier et de la dispersion des points
plt.figure(figsize=(16,14))
plt.errorbar(l[:,3],l[:,2],fmt='+',yerr=2e-2*l[:,2],label='Points')
plt.plot(l[:,3],fitfunc(l[:,3],p[0],p[1]),label='Fit')
plt.plot(l[:,3],fitfunc(l[:,3],p3[0],p3[1]),label='Fit corrigé')
plt.errorbar(l[:,3],l[:,2]*1e5/fitfunc2(l[:,3],p2[0],p2[1],p2[2],p2[3],p2[4],p2[5],p2[6]),fmt='+',yerr=2e-2*l[:,2],label='Points corrigées')
plt.xlabel('Champ magnétique (T)')
plt.ylabel('Aimantation*mu0 (T)')
plt.title("Aimantation multipliée par mu0 en fonction du champ magnétique")
plt.legend()
plt.show()