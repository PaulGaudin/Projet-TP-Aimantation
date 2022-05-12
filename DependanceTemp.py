import numpy as np
import matplotlib.pyplot as plt
import fileinput
from math import exp 
from scipy import optimize
from scipy import odr


def fitfunc(z,a,b,c,d,e,f,g):
    return a + b*z + c*z*z + d*z*z*z + e*z*z*z*z + f*z*z*z*z*z + g*pow(z,0.5)


#Récupération du modèle précédemment déterminé de T(R)
def Modele(T,a,b,c):
    return a*T*T+b*T+c

p=np.loadtxt(f'Modele_T.txt')


Nbmesures=1

#Affichage de toute les mesures de A en fonction de T a z fixé, pour différent z
plt.figure()
for i in range(Nbmesures):
    f = open(f'Temp{i}.txt','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace(",",".")
    f = open(f'Temp{i}.txt','w')
    f.write(newdata)
    f.close()
    l=np.loadtxt(f'Temp{i}.txt')
    l[:,0]*=1e-9
    
    plt.errorbar(Modele(l[:,4],p[0],p[1],p[2]),l[:,0],fmt='+',label=f'z = {l[5,1]}')

    """
    p0=(1,1,1,1,1,1,1)
    p, cv = optimize.curve_fit(fitfunc,l[:,5],l[:,0],p0)
    plt.plot(l[:,5],fitfunc(l[:,5],p[0],p[1],p[2],p[3],p[4],p[5],p[6]),label=f'Fit z = {l[5,1]}')
    """


plt.title(f"Variation de l'aimantation en fonction de la température")
plt.xlabel('Température (K)')
plt.ylabel('Aimantation (A/m)')
plt.legend()
plt.show()

