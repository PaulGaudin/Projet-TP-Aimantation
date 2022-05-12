import numpy as np
import matplotlib.pyplot as plt
import fileinput
from math import exp 
from scipy import optimize
from scipy import odr

#Conversion des , en . pour pouvoir récupérer les données
f = open('Godolinium6.txt','r')
filedata = f.read()
f.close()
newdata = filedata.replace(",",".")
f = open('Godolinium6.txt','w')
f.write(newdata)
f.close()

#Chargement des données
l=np.loadtxt('Godolinium6.txt')
l[:,0]*=1e-9

#Creation d'un fit par une loi affine (Cf ...)
def fitfunc(z,b,a):
    return a+b*z

p0=(1,1)
p, cv = optimize.curve_fit(fitfunc,l[:,3],l[:,2],p0)
print(f"Chi = {p[0]}")

#Affichage des données et du plot pour vérification de la qualité de ce dernier et de la dispersion des points
plt.figure()
plt.plot(l[:,3],fitfunc(l[:,3],p[0],p[1]))
plt.errorbar(l[:,3],l[:,2],fmt='+')
plt.show()