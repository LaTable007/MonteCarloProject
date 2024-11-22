import numpy as np
import matplotlib.pyplot as plt


# Constants

crossSectionAbsorp = 0.2 # Définition d'une valeur pour la cross Section d'absorption pas tenir compte des dimensions pour l'instant 
crossSectionScatter = 0.8 # Même chose pour la cross Section de diffusion
numberPoints = 1000 # Nombre de neutrons envoyé
thicknessWall = 1.5 # Épaisseur de la paroi

pos = np.zeros((numberPoints, 2)) # Position initiale des neutrons
direction = np.zeros((numberPoints, 2)) # Direction initiale des neutrons
direction[:, 0] = 1

i = 0
numberAbsorp = 0 # Nombre de neutrons absorbés ou qui sont sortie du mur
numberPointsOutside = 0 # Nombre de neutrons qui sont derrière le mur
numberPointsBackScatter = 0 # Nombre de neutrons qui sont devant le mur

while numberAbsorp < numberPoints: # Tant que tous les neutrons n'ont pas été absorbés ou sont sorties du mur
    i = 0
    while i < numberPoints: # On vérifie pour tous les neutrons
        if np.all(direction[i, :] == 0): # En gros quand un neutron est absorbé sort du mur ou est absorbé il est désactivé ce qui revient à lui donner une direction nulle et de le skipp dés qu'on le croise '
            i += 1
            continue
        ethaAbsorp = np.random.uniform(0, 1, 1) # Génération d'un nombre aléatoire entre 0 et 1
        ethaScatter = np.random.uniform(0, 1, 1) # Génération d'un nombre aléatoire entre 0 et 1
    
        sampleAbsorp = -np.log(ethaAbsorp) / crossSectionAbsorp # Calcul de la distance parcourue avant absorption
        sampleScatter = -np.log(ethaScatter) / crossSectionScatter # Calcul de la distance parcourue avant diffusion


        if pos[i, 0] > thicknessWall: # Si le neutron est derrière le mur
            numberPointsOutside += 1 # On incrémente le nombre de neutrons derrière le mur
            numberAbsorp += 1 # On incrémente le nombre de neutrons absorbés
            print(numberAbsorp)
            direction[i, :] = [0, 0]  # Désactive le neutron
            i += 1
            continue
        
        if pos[i, 0] < 0: # Si le neutron est devant le mur
            numberPointsBackScatter += 1 # On incrémente le nombre de neutrons devant le mur
            numberAbsorp += 1 # On incrémente le nombre de neutrons absorbés
            print(numberAbsorp)
            direction[i, :] = [0, 0]  # Désactive le neutron
            i += 1
            continue
        
        if sampleAbsorp < sampleScatter: # Si la distance parcourue avant absorption est plus petite que celle avant diffusion alors on considère que le neutron est absorbé
            pos[i, :] = pos[i, :] + sampleAbsorp * direction[i, :] # On met à jour la position du neutron
            direction[i, :] = [0, 0] # On désactive le neutron
            numberAbsorp += 1 # On incrémente le nombre de neutrons absorbés
            print(numberAbsorp)
    
        else: # Sinon le neutron est diffusé
            theta = np.random.uniform(0, 2 * np.pi, 1)[0] # On génère un angle aléatoire entre 0 et 2pi
            direction[i, :] = [np.cos(theta), np.sin(theta)] # On met à jour la direction du neutron
            pos[i, :] = pos[i, :] + sampleScatter * direction[i, :] # On met à jour la position du neutron

        i += 1


print('Number of points: ', numberPoints)
print('Number of points outside: ', numberPointsOutside)
print('Number of points backscattered: ', numberPointsBackScatter)

# Step 2 - Draw it's free flight

# Step 3 - Draw the type of collision

# Step 4 - Deal with next n in memory (if appropriate) and go to 2

# Step 5 - Go to 1 if there are still runs to play

x_limits = (thicknessWall - thicknessWall*1.5, thicknessWall*1.5)
y_limits = (-thicknessWall*1.5, thicknessWall*1.5)

plt.hist2d(pos[:, 0], pos[:, 1], bins=100, range=[x_limits, y_limits], cmap='viridis')
plt.colorbar(label='Densité des points')


plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Début de la région')
plt.axvline(x=thicknessWall, color='red', linestyle='--', linewidth=2, label='Fin de la région')

plt.xlabel('Position en X')
plt.ylabel('Position en Y')
plt.title('Répartition des points dans le plan')
plt.show()
