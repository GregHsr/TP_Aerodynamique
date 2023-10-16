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

def coef_pression(Liste_pression,vitesse):
    Liste_coefficient = []
    for i in range(len(Liste_pression)):
        Liste_coefficient.append(Liste_pression[i]/(0.5*1.204*vitesse**2))
    return Liste_coefficient

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

# Rapport portance / traînée

Liste_rapport_angle = []
for i in range(len(Angle_alpha)):
    Liste_rapport_angle.append(Liste_resultante_portance[i]/Liste_resultante_trainee[i])

# Calcul du coefficient de pression

Liste_coefficient_angle = []
for i in range(len(Angle_alpha)):
    Liste_coefficient_angle.append(coef_pression(data_angle[6+i],15))

#print("Liste des résultantes de portance pour chaque angle :", Liste_resultante_portance)
#print("Liste des résultantes de traînée pour chaque angle :", Liste_resultante_trainee)

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

# Rapport portance / traînée

Liste_rapport_vitesse = []
for i in range(len(vitesse)):
    Liste_rapport_vitesse.append(Liste_resultante_portance_vitesse[i]/Liste_resultante_trainee_vitesse[i])

# Calcul du coefficient de pression

Liste_coefficient_vitesse = []
for i in range(len(vitesse)):
    Liste_coefficient_vitesse.append(coef_pression(data_vitesse[6+i],vitesse[i]))

#print("Liste des résultantes de portance pour chaque vitesse :", Liste_resultante_portance_vitesse)
#print("Liste des résultantes de traînée pour chaque vitesse :", Liste_resultante_trainee_vitesse)

# Tracé du profil d'aile

Liste_point_mesure = [0,2,3,4,5,7,11,15,18,27,28,29,30,31,33,34,36,38,42,49,55]
plt.figure(1)
plt.plot(data_angle[1], data_angle[2],'o',label = "Proints interpolés")
plt.plot([data_angle[1][k] for k in Liste_point_mesure], [data_angle[2][k] for k in Liste_point_mesure],'o',label = "Points de mesure")
v = plt.quiver(data_angle[1], data_angle[2], [np.cos(k) for k in data_vitesse[4]], [np.sin(k) for k in data_vitesse[4]],scale=0.05,scale_units='xy',headwidth=2)
plt.quiverkey(v, 0.8, 0.75, 2, label=r"$t_l$", coordinates = "axes")
plt.axis('equal')
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

# Tracé de la portance et de la traînée en fonction de l'angle d'attaque

plt.figure(2)
plt.subplot(121)
plt.plot(Angle_alpha, Liste_resultante_portance,'o',color = "orange",label = r"$F_z$")
plt.xlabel(r"$\alpha$ [rad]")
plt.legend()
plt.ylabel("Portance [N/m]")
plt.subplot(122)
plt.plot(Angle_alpha, Liste_resultante_trainee,'o',color = "orange",label = r"$F_x$")
plt.xlabel(r"$\alpha$ [rad]")
plt.ylabel("Traînée [N/m]")
plt.legend()

# Tracé de la portance et de la traînée en fonction de la vitesse
plt.figure(3)
plt.subplot(121)
plt.plot(vitesse, Liste_resultante_portance_vitesse,'o',color = "orange",label = r"$F_z$")
plt.xlabel("Vitesse [m/s]")
plt.legend()
plt.ylabel("Portance [N/m]")
plt.subplot(122)
plt.plot(vitesse, Liste_resultante_trainee_vitesse,'o',color = "orange",label = r"$F_x$")
plt.axis('equal')
plt.xlabel("Vitesse [m/s]")
plt.ylabel("Traînée [N/m]")
plt.legend()

# Tracé du rapport portance / traînée en fonction de l'angle d'attaque
plt.figure(4)
plt.plot(Angle_alpha, Liste_rapport_angle,'o',color = "orange",label = r"$\frac{F_z}{F_x}$")
plt.xlabel(r"$\alpha$ [rad]")
plt.ylabel(r"$\frac{F_z}{F_x}$")
plt.legend()

# Tracé du rapport portance / traînée en fonction de la vitesse
plt.figure(5)
plt.plot(vitesse, Liste_rapport_vitesse,'o',color = "orange",label = r"$\frac{F_z}{F_x}$")
plt.xlabel("Vitesse [m/s]")
plt.ylabel(r"$\frac{F_z}{F_x}$")
plt.legend()

# Tracé des coefs de pression en fonction de l'angle d'attaque
plt.figure(6)
plt.subplot(231)
plt.plot(data_angle[3][:28], Liste_coefficient_angle[0][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_angle[0][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$\alpha = 0°$")
plt.legend()
plt.subplot(232)
plt.plot(data_angle[3][:28], Liste_coefficient_angle[1][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_angle[1][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$\alpha = 4°$")
plt.legend()
plt.subplot(233)
plt.plot(data_angle[3][:28], Liste_coefficient_angle[2][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_angle[2][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$\alpha = 7°$")
plt.legend()
plt.subplot(234)
plt.plot(data_angle[3][:28], Liste_coefficient_angle[3][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_angle[3][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$\alpha = 10°$")
plt.legend()
plt.subplot(235)
plt.plot(data_angle[3][:28], Liste_coefficient_angle[4][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_angle[4][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$\alpha = 13°$")
plt.legend()
plt.subplot(236)
plt.plot(data_angle[3][:28], Liste_coefficient_angle[5][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_angle[5][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$\alpha = 16°$")
plt.legend()

#Tracé des coefs de pression en fonction de la vitesse
plt.figure(7)
plt.subplot(231)
plt.plot(data_angle[3][:28], Liste_coefficient_vitesse[0][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_vitesse[0][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$U_0 = 10 m/s$")
plt.legend()
plt.subplot(232)
plt.plot(data_angle[3][:28], Liste_coefficient_vitesse[1][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_vitesse[1][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$U_0 = 13.2 m/s$")
plt.legend()
plt.subplot(233)
plt.plot(data_angle[3][:28], Liste_coefficient_vitesse[2][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_vitesse[2][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$U_0 = 16.35 m/s$")
plt.legend()
plt.subplot(234)
plt.plot(data_angle[3][:28], Liste_coefficient_vitesse[3][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_vitesse[3][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$U_0 = 19.15 m/s$")
plt.legend()
plt.subplot(235)
plt.plot(data_angle[3][:28], Liste_coefficient_vitesse[4][:28],'--o',color = "orange",label = "extrados")
plt.plot(data_angle[3][28:], Liste_coefficient_vitesse[4][28:],'--o',color = "blue",label = "intrados")
plt.xlabel("x")
plt.ylabel(r"$C_p$")
plt.title(r"$U_0 = 22.8 m/s$")
plt.legend()

# Tracé de la force aérodynamique 

Pression_0=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    Pression_0[i]=data_angle[6][i]/(0.5*1.29*15)
    
Pression_4=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    Pression_4[i]=data_angle[7][i]/(0.5*1.29*15)
    
Pression_7=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    Pression_7[i]=data_angle[8][i]/(0.5*1.29*15)

Pression_10=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    Pression_10[i]=data_angle[9][i]/(0.5*1.29*15)
    
Pression_13=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    Pression_13[i]=data_angle[10][i]/(0.5*1.29*15)
    
Pression_16=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    Pression_16[i]=data_angle[11][i]/(0.5*1.29*15)

listes_de_Pression=[Pression_0,Pression_4,Pression_7,Pression_10,Pression_13,Pression_16]    
# Trace le champ de pression autour de l'aile avec des couleurs différentes
fig, axs = plt.subplots(3,2, figsize=(6, 10))

for i in range (6):  
    row, col = divmod(i, 2)  # Calcule la ligne et la colonne pour le sous-graphique actuel
    ax = axs[row, col]  # Sélectionne le sous-graphique actuel
    
    ax.set_xlim(-20, 380)
    ax.set_ylim(-100, 100)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f'Angle {i}')  # Titre du sous-graphique
    plt.plot(data_angle[1], data_angle[2],'o',label = "Profil d'aile")
    for j in range(len(listes_de_Pression[i])):
        if listes_de_Pression[i][j] > 0:
            ax.plot(data_angle[1][j], data_angle[2][j], 'x', color='green')
            
        else:
            ax.plot(data_angle[1][j], data_angle[2][j], 'x', color='red')

plt.tight_layout()  # Régle les espaces entre les sous-graphiques

FPression_0_n=[0 for i in range(len(data_angle[1]))]
FPression_0_t=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    FPression_0_n[i]=-data_angle[6][i]*data_angle[5][i]*np.cos(data_angle[4][i]*np.pi/180)
    FPression_0_t[i]=data_angle[6][i]*data_angle[5][i]*np.sin(data_angle[4][i]*np.pi/180)

FPression_4_n=[0 for i in range(len(data_angle[1]))]
FPression_4_t=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    FPression_4_n[i]=-data_angle[7][i]*data_angle[5][i]*np.cos(data_angle[4][i]*np.pi/180)
    FPression_4_t[i]=data_angle[7][i]*data_angle[5][i]*np.sin(data_angle[4][i]*np.pi/180)

FPression_7_n=[0 for i in range(len(data_angle[1]))]
FPression_7_t=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    FPression_7_n[i]=-data_angle[8][i]*data_angle[5][i]*np.cos(data_angle[4][i]*np.pi/180)
    FPression_7_t[i]=data_angle[8][i]*data_angle[5][i]*np.sin(data_angle[4][i]*np.pi/180)

FPression_10_n=[0 for i in range(len(data_angle[1]))]
FPression_10_t=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    FPression_10_n[i]=-data_angle[9][i]*data_angle[5][i]*np.cos(data_angle[4][i]*np.pi/180)
    FPression_10_t[i]=data_angle[9][i]*data_angle[5][i]*np.sin(data_angle[4][i]*np.pi/180)    

FPression_13_n=[0 for i in range(len(data_angle[1]))]
FPression_13_t=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    FPression_13_n[i]=-data_angle[10][i]*data_angle[5][i]*np.cos(data_angle[4][i]*np.pi/180)
    FPression_13_t[i]=data_angle[10][i]*data_angle[5][i]*np.sin(data_angle[4][i]*np.pi/180)

FPression_16_n=[0 for i in range(len(data_angle[1]))]
FPression_16_t=[0 for i in range(len(data_angle[1]))]
for i in range(len(data_angle[1])):
    FPression_16_n[i]=-data_angle[11][i]*data_angle[5][i]*np.cos(data_angle[4][i]*np.pi/180)
    FPression_16_t[i]=data_angle[11][i]*data_angle[5][i]*np.sin(data_angle[4][i]*np.pi/180)

n_loc=[]
FPression_160_n=[0 for i in range(len(data_angle[1]))]

plt.quiver(data_angle[1], data_angle[2], FPression_0_t, FPression_0_n, scale=5, color='black', label='Forces de pression')
plt.quiver(data_angle[1], data_angle[2], FPression_4_t, FPression_4_n, scale=5, color='blue', label='Forces de pression')
plt.quiver(data_angle[1], data_angle[2], FPression_7_t, FPression_7_n, scale=5, color='red', label='Forces de pression')
plt.quiver(data_angle[1], data_angle[2], FPression_10_t, FPression_10_n, scale=5, color='pink', label='Forces de pression')
plt.quiver(data_angle[1], data_angle[2], FPression_13_t, FPression_13_n, scale=5, color='violet', label='Forces de pression')
plt.quiver(data_angle[1], data_angle[2], FPression_16_t, FPression_16_n, scale=5, color='g', label='Forces de pression')

for i in range (6):  
    row, col = divmod(i, 2)  # Calcule la ligne et la colonne pour le sous-graphique actuel
    ax = axs[row, col]  # Sélectionne le sous-graphique actuel
    
    ax.set_xlim(-20, 380)
    ax.set_ylim(-100, 100)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f'Angle {i}')  # Titre du sous-graphique
    plt.plot(data_angle[1], data_angle[2],'o',label = "Profil d'aile")
    for j in range(len(listes_de_Pression[i])):
        if listes_de_Pression[i][j] > 0:
            ax.plot(data_angle[1][j], data_angle[2][j], 'x', color='green')
            
        else:
            ax.plot(data_angle[1][j], data_angle[2][j], 'x', color='red')

plt.tight_layout()  # Régle les espaces entre les sous-graphiques
                 
# Données pour les composantes tangentielle et normale à l'aile
indices = [0, 4, 7, 10, 13, 16]
colors = ['black', 'black', 'black', 'black', 'black', 'black']  # Couleurs pour les vecteurs
x = data_angle[1]  # Coordonnées x des points d'application des forces
y = data_angle[2]  # Coordonnées y des points d'application des forces

# Crée une figure et une grille de sous-graphiques
fig, axs = plt.subplots(2, 3, figsize=(12, 8))

k=30
i,idx=0,0

row, col = divmod(i, 3)  # Calcule la ligne et la colonne pour le sous-graphique actuel
axs[row, col].plot(data_angle[1], data_angle[2],'x')
tangentielle = FPression_0_t  # Remplace par les données correctes pour chaque indice
normale = FPression_0_n  # Remplace par les données correctes pour chaque indice
label = f'Forces de pression'
axs[row, col].quiver(x, y, tangentielle, normale, scale=k, color=colors[i], label=label)
axs[row, col].quiver(125, 0,0.13,3.43, scale=k, color="red", label="Force Aérodynamique")
axs[row, col].set_title(f'Angle de {idx}°')
axs[row, col].set_ylim(-100, 200)
axs[row, col].set_xlim(-10, 380)

i,idx=1,4
row, col = divmod(i, 3)  # Calcule la ligne et la colonne pour le sous-graphique actuel
axs[row, col].plot(data_angle[1], data_angle[2],'x')
tangentielle = FPression_4_t  # Remplace par les données correctes pour chaque indice
normale = FPression_4_n  # Remplace par les données correctes pour chaque indice
label = f'Forces de pression'
axs[row, col].quiver(x, y, tangentielle, normale, scale=k, color=colors[i], label=label)
axs[row, col].quiver(125, 0,0.47,17.82, scale=k, color="red", label="Force Aérodynamique")
axs[row, col].set_title(f'Angle de {idx}°')
axs[row, col].set_ylim(-100, 200)
axs[row, col].set_xlim(-10, 380)

i,idx=2,7
row, col = divmod(i, 3)  # Calcule la ligne et la colonne pour le sous-graphique actuel
axs[row, col].plot(data_angle[1], data_angle[2],'x')
tangentielle = FPression_7_t  # Remplace par les données correctes pour chaque indice
normale = FPression_7_n  # Remplace par les données correctes pour chaque indice
label = f'Forces de pression'
axs[row, col].quiver(x, y, tangentielle, normale, scale=k, color=colors[i], label=label)
axs[row, col].quiver(125, 0,1.12,27.65, scale=k, color="red", label="Force Aérodynamique")
axs[row, col].set_title(f'Angle de {idx}°')
axs[row, col].set_ylim(-100, 200)
axs[row, col].set_xlim(-10, 380)

i,idx=3,10
row, col = divmod(i, 3)  # Calcule la ligne et la colonne pour le sous-graphique actuel
axs[row, col].plot(data_angle[1], data_angle[2],'x')
tangentielle = FPression_10_t  # Remplace par les données correctes pour chaque indice
normale = FPression_10_n  # Remplace par les données correctes pour chaque indice
label = f'Forces de pression'
axs[row, col].quiver(x, y, tangentielle, normale, scale=k, color=colors[i], label=label)
axs[row, col].quiver(125, 0,1.87,39.27, scale=k, color="red", label="Force Aérodynamique")
axs[row, col].set_title(f'Angle de {idx}°')
axs[row, col].set_ylim(-100, 200)
axs[row, col].set_xlim(-10, 380)

i,idx=4,13
row, col = divmod(i, 3)  # Calcule la ligne et la colonne pour le sous-graphique actuel
axs[row, col].plot(data_angle[1], data_angle[2],'x')
tangentielle = FPression_13_t  # Remplace par les données correctes pour chaque indice
normale = FPression_13_n  # Remplace par les données correctes pour chaque indice
label = f'Forces de pression'
axs[row, col].quiver(x, y, tangentielle, normale, scale=k, color=colors[i], label=label)
axs[row, col].quiver(125, 0,6.14,39.8, scale=k, color="red", label="Force Aérodynamique")
axs[row, col].set_title(f'Angle de {idx}°')
axs[row, col].set_ylim(-100, 200)
axs[row, col].set_xlim(-10, 380)

i,idx=5,16
row, col = divmod(i, 3)  # Calcule la ligne et la colonne pour le sous-graphique actuel
axs[row, col].plot(data_angle[1], data_angle[2],'x')
tangentielle = FPression_16_t  # Remplacezpar les données correctes pour chaque indice
normale = FPression_16_n  # Remplace par les données correctes pour chaque indice
label = f'Forces de pression'
axs[row, col].quiver(x, y, tangentielle, normale, scale=k, color=colors[i], label=label)
axs[row, col].quiver(125, 0,12.32,37.8, scale=k, color="red", label="Force Aérodynamique")
axs[row, col].set_title(f'Angle de {idx}°')
axs[row, col].set_ylim(-100, 200)
axs[row, col].set_xlim(-10, 380)

for ax in axs.flat:
    ax.legend()

plt.tight_layout()

plt.show()

