import numpy as np
import matplotlib.pyplot as plt
import fileinput
from math import exp
from scipy import optimize
from scipy import odr


def fitfunc(T,a,b,c,d):
    return a*pow(1-1/pow(np.sinh(b/T),4),1/8) +c*np.exp(T*d)


#Récupération du modèle précédemment déterminé de T(R)
def Modele(T,a,b,c):
    return a*T*T+b*T+c

p2=np.loadtxt(f'Data/Modele_T.txt')


Nbmesures=4

#Affichage de toute les mesures de A en fonction de T a z fixé, pour différent z
plt.figure(figsize=(16,14))
for i in range(Nbmesures):
    f = open(f'Data/Temp{i}.txt','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace(",",".")
    f = open(f'Data/Temp{i}.txt','w')
    f.write(newdata)
    f.close()
    l=np.loadtxt(f'Data/Temp{i}.txt')
    l[:,0]*=1e-9
    
    plt.errorbar(Modele(l[:,4],p2[0],p2[1],p2[2]),l[:,0],fmt='+',label=f'z = {l[5,1]}')

    
    p0=(1,1,1,1)
    p, cv = optimize.curve_fit(fitfunc,Modele(l[:,4],p2[0],p2[1],p2[2]),l[:,0],p0,maxfev=1000)
    print(p)
    plt.plot(Modele(l[:,4],p2[0],p2[1],p2[2]),fitfunc(Modele(l[:,4],p2[0],p2[1],p2[2]),p[0],p[1],p[2],p[3]),label=f'Fit z = {l[5,1]}')
    
    


plt.title(f"Variation de l'aimantation en fonction de la température")
plt.xlabel('Température (K)')
plt.ylabel('Aimantation (A/m)')
plt.legend()
plt.show()

