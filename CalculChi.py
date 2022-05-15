import numpy as np
import matplotlib.pyplot as plt
import fileinput
from scipy import optimize
from scipy import odr
from decimal import Decimal

mu0=1.2566e-6
#Conversion des , en . pour pouvoir récupérer les données
f = open('Data/GadSulfOctH.txt','r')
filedata = f.read()
f.close()
newdata = filedata.replace(",",".")
f = open('Data/GadSulfOctH.txt','w')
f.write(newdata)
f.close()

l=np.loadtxt('Data/GadSulfOctH.txt')
l[:,0]*=1e-9

p2=np.loadtxt(f'Data/Modele_A.txt')

#Creation de la fonction permettant de calculer Chi en fonction de z
def B(z):
    B0=56.190
    z1=-0.59179
    z2=-0.58146
    R=1.4938
    return B0*((z-z1)/pow((pow(z-z1,2)+pow(R,2)),0.5)-(z-z2)/pow((pow(z-z2,2)+pow(R,2)),0.5))*1e-3


def func(z,M,B):

    return mu0*M/B(z)*(mu0*M/B(z)+1)

#Creation d'une fonction de fit, et determination de ses paramètres
def fitfunc(z,a,b,c,d,e,f,g):
    return a + b*z + c*z*z + d*z*z*z + e*z*z*z*z + f*z*z*z*z*z + g*pow(z,0.5)

def fitfunc2(z,a,b):
    return z*a+b

p0=(1,1,1,1,1,1,1)
p, cv = optimize.curve_fit(fitfunc,l[:,1],l[:,0],p0)

#Creation d'une fonction corrigeant les valeurs de l'aimantation obtenues par celles obtenues pour l'aimant permanent (Cf ...)
def finalfunc(z,p,p2):
    return 1e5*fitfunc(z,p[0],p[1],p[2],p[3],p[4],p[5],p[6])/fitfunc(z,p2[0],p2[1],p2[2],p2[3],p2[4],p2[5],p2[6])

#Affichages des courbes obtenues

plt.figure(figsize=(16,14))
plt.subplot(1,2,1)
plt.plot(l[:,1],fitfunc(l[:,1],p[0],p[1],p[2],p[3],p[4],p[5],p[6]),label='Fit')
plt.plot(l[:,1],finalfunc(l[:,1],p,p2),label='Fit corrigé')
plt.errorbar(l[:,1],l[:,0],fmt='+')
plt.title('Aimantation en fonction de la hauteur')
plt.xlabel('Hauteur (cm)')
plt.ylabel('Aimantation (A/m)')
plt.legend()

plt.subplot(1,2,2)

#Creation d'une fonction corrigeant les valeurs de Xm obtenues 

p0=(1,1)
p3, cv = optimize.curve_fit(fitfunc2,l[:,1],func(l[:,1],l[:,0],B),p0)
p4, cv = optimize.curve_fit(fitfunc2,l[:,1],func(l[:,1],finalfunc(l[:,1],p,p2),B),p0)

def finalfunc2(z,p,p2):
    return 1e5*fitfunc2(z,p[0],p[1])/fitfunc(z,p2[0],p2[1],p2[2],p2[3],p2[4],p2[5],p2[6])

#Affichage des courbes

plt.errorbar(l[:,1],func(l[:,1],l[:,0],B),fmt='+')
plt.plot(l[:,1],fitfunc2(l[:,1],p3[0],p3[1]),label='Fit')
plt.plot(l[:,1],fitfunc2(l[:,1],p4[0],p4[1]),label='Fit corrigé')
plt.title('Susceptibilité magnétique en fonction de la hauteur')
plt.xlabel('Hauteur (cm)')
plt.ylabel('Suscéptibilité magnétique')
plt.legend()
plt.show()
