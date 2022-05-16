import numpy as np
import matplotlib.pyplot as plt
import fileinput
from scipy import optimize
from scipy import odr
from decimal import Decimal

#On utilise ce programme uniquement pour calculer la susceptibilité magnétique du laiton, car le tableau de valeur est incomplet pour ce matériau

mu0=1.2566e-6

l=np.loadtxt('Data/laiton.txt')

def B(z):
    B0=56.190
    z1=-0.59179
    z2=-0.58146
    R=1.4938
    return B0*((z-z1)/pow((pow(z-z1,2)+pow(R,2)),0.5)-(z-z2)/pow((pow(z-z2,2)+pow(R,2)),0.5))*1e-3

Field=B(l[:,1])

A=l[:,0]*mu0*1e-11

#Creation d'un fit par une loi affine et ajutsement des points par la courbe de l'iamant permanent (Cf ...)
def fitfunc(z,b,a):
    return a+b*z

p2=np.loadtxt(f'Data/Modele_A.txt')

def fitfunc2(z,a,b,c,d,e,f,g):
    return a + b*z + c*z*z + d*z*z*z + e*z*z*z*z + f*z*z*z*z*z + g*pow(z,0.5)

def finalfunc(z,p,p2):
    return 1e5*fitfunc(z,p[0],p[1])/fitfunc2(z,p2[0],p2[1],p2[2],p2[3],p2[4],p2[5],p2[6])

p0=(1,1)
p, cv = optimize.curve_fit(fitfunc,Field,A,p0,maxfev=10000)
print(f"Chi = {p[0]}")

p0=(1,1)
p3, cv = optimize.curve_fit(fitfunc,Field,A*1e5/fitfunc2(Field,p2[0],p2[1],p2[2],p2[3],p2[4],p2[5],p2[6]),p0,maxfev=10000)
print(f"Chi corrigé = {p3[0]}")

#Affichage des données et du plot pour vérification de la qualité de ce dernier et de la dispersion des points
plt.figure(figsize=(16,14))
plt.plot(Field,fitfunc(Field,p[0],p[1]),label='Fit')

plt.errorbar(Field,A,fmt='+',yerr=2e-2*A,label='Points')
plt.errorbar(Field,A*1e5/fitfunc2(Field,p2[0],p2[1],p2[2],p2[3],p2[4],p2[5],p2[6]),fmt='+',yerr=2e-2*A,label='Points corrigées')
plt.plot(Field,fitfunc(Field,p3[0],p3[1]),label='Fit corrigé')
plt.xlabel('Champ magnétique (T)')
plt.ylabel('Aimantation*mu0 (T)')
plt.title("Aimantation multipliée par mu0 en fonction du champ magnétique")
plt.legend()
plt.show()