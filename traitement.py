import os
import numpy as np
import matplotlib.pyplot as plt

# Fonction lecture fichier

def lecture_fichier(nom_fichier):
    with open(nom_fichier, "r") as fichier:
        nom_colonne = fichier.readline().split(",")
        for i in range(len(nom_colonne)):
            nom_colonne[i] = []
        for ligne in fichier:
            ligne = ligne.split(",")
            if ligne[0] != "Position":
                for i in range(len(ligne)):
                    nom_colonne[i].append(float(ligne[i]))
    return [nom_colonne[i] for i in range(len(nom_colonne))]

def conv_deg_rad(liste_angle):
    for i in range(len(liste_angle)):
        liste_angle[i] = liste_angle[i]*np.pi/180
    return liste_angle

def calcul_portance(pression, angle_alpha, angle_beta, longueur):
    portance = []
    for k in range(len(pression)): 
        portance.append(-pression[k]*longueur[k]*np.cos(angle_alpha - angle_beta[k]))
    return portance

def calcul_trainee(pression, angle_alpha, angle_beta, longueur):
    traînée = []
    for k in range(len(pression)): 
        traînée.append(-pression[k]*longueur[k]*np.sin(angle_alpha - angle_beta[k]))
    return traînée

def resultante(liste):
    somme = 0
    for i in range(len(liste)):
        somme += liste[i]
    return somme

# Analyse pour différents angles

data_angle = lecture_fichier("TPAERO_angle.csv")

Angle_alpha = conv_deg_rad([0,4,7,10,13,16])

Liste_Portance = []
Liste_Trainee = []
Liste_resultante_portance = []
Liste_resultante_trainee = []

for i in range(len(Angle_alpha)):
    Liste_Portance.append(calcul_portance(data_angle[6+i], Angle_alpha[i], data_angle[4], data_angle[5]))
    Liste_Trainee.append(calcul_trainee(data_angle[6+i], Angle_alpha[i], data_angle[4], data_angle[5]))

    Liste_resultante_portance.append(resultante(Liste_Portance[i]))
    Liste_resultante_trainee.append(resultante(Liste_Trainee[i]))

#print("Liste des résultantes de portance pour chaque angle :", Liste_resultante_portance)
#print("Liste des résultantes de traînée pour chaque angle :", Liste_resultante_trainee)

# Tracé du profil d'aile

plt.figure(1)
plt.plot(data_angle[1], data_angle[2],'o',label = "Profil d'aile")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

# Analyse pour différentes vitesses

data_vitesse = lecture_fichier("TPAERO_vitesse.csv")

vitesse = [10,13.2,16.35,19.15,22.8]
alpha_vitesse = 10*np.pi/180

Liste_Portance_vitesse = []
Liste_Trainee_vitesse = []
Liste_resultante_portance_vitesse = []
Liste_resultante_trainee_vitesse = []

for i in range(len(vitesse)):
    Liste_Portance_vitesse.append(calcul_portance(data_vitesse[6+i], alpha_vitesse, data_vitesse[4], data_vitesse[5]))
    Liste_Trainee_vitesse.append(calcul_trainee(data_vitesse[6+i], alpha_vitesse, data_vitesse[4], data_vitesse[5]))

    Liste_resultante_portance_vitesse.append(resultante(Liste_Portance_vitesse[i]))
    Liste_resultante_trainee_vitesse.append(resultante(Liste_Trainee_vitesse[i]))

print("Liste des résultantes de portance pour chaque vitesse :", Liste_resultante_portance_vitesse)
print("Liste des résultantes de traînée pour chaque vitesse :", Liste_resultante_trainee_vitesse)