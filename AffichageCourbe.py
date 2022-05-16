import numpy as np
import matplotlib.pyplot as plt
import fileinput
from scipy import optimize
from scipy import odr


kb=1.380649e-23

#Récupération des données de callibrage de la hauteur en fonction de la tension mesurée
l=np.loadtxt('Data/Calib_H.txt')


plt.figure(figsize=(16,14))

plt.subplot(1,2,1)

#Creation du fit des points de callibrage pour déterminer la loi qui lie la tension mesurée et la hauteur de l'échantillon
def fit():
    p0=(0,0)
    params, cv = optimize.curve_fit(lambda t,a,b:a*t+b,l[:,1],l[:,0],p0)
    return params

a,b=fit()
#Affichage de la courbe et de son fit
plt.plot(l[:,1],l[:,0],'+')
plt.errorbar(l[:,1],l[:,0],xerr=0.00025,yerr=0.01,fmt='+')
plt.plot(l[:,1],a*l[:,1]+b,label='Fit')
plt.title("Tension mesurée en fonction de la hauteur de l'échantillon")
print(f"a= {a}, b = {b}\n")
plt.xlabel('Hauteur (m)')
plt.ylabel('Tension (V)')
plt.legend()


#Transformation et récupération des données de callibrage du champ en fonction de la hauteur
f = open('Data/Donnees_Calib.txt','r')
filedata = f.read()
f.close()
newdata = filedata.replace(",",".")
f = open('Data/Donnees_Calib.txt','w')
f.write(newdata)
f.close()

l=np.loadtxt('Data/Donnees_Calib.txt')
l[:,0]*=1e-3
nbmesures=159
plt.subplot(1,2,2)

#Création de la fonction de fit des points
def B(z,B0,z1,z2,R):
    return B0*((z-z1)/pow((pow(z-z1,2)+pow(R,2)),0.5)-(z-z2)/pow((pow(z-z2,2)+pow(R,2)),0.5))

def fit(fitfunc,S,Hshift,Bshift):
    p0=(2859.7,-3.3854,0.43022,1.3568)
    params, cv = optimize.curve_fit(B,l[:,1]+Bshift,l[:,0]+Hshift,p0,sigma=S,maxfev=100000)
    return params


#Affichage de la courbe et de son fit
B0,z1,z2,R=fit(B,np.ones(nbmesures)*1e-4,0,0)
plt.errorbar(l[:,1],l[:,0],xerr=0.1,yerr=1e-4,fmt='+')
plt.plot(l[:,1],B0*((l[:,1]-z1)/pow((pow(l[:,1]-z1,2)+pow(R,2)),0.5)-(l[:,1]-z2)/pow((pow(l[:,1]-z2,2)+pow(R,2)),0.5)),label='Fit')
plt.title(f"Champ mesuré en fonction de la hauteur")
print(f"B0 = {B0}, z1 = {z1}, z2 = {z2}, R = {R}\n")
plt.yscale("log")
plt.grid(True, which='both')
plt.xlabel('Hauteur (cm)')
plt.ylabel('Champ B (T)')
plt.legend()
plt.show()