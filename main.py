import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm 
from utils import printProgressBar


# Constants

crossSectionAbsorp = 1 # Définition d'une valeur pour la cross Section d'absorption pas tenir compte des dimensions pour l'instant 
crossSectionScatter = 67 # Même chose pour la cross Section de diffusion
numberPoints = 100000 # Nombre de neutrons envoyé
thicknessWall = 0.1 # Épaisseur de la paroi

pos = np.zeros((numberPoints, 2)) # Position initiale des neutrons
direction = np.zeros((numberPoints, 2)) # Direction initiale des neutrons
direction[:, 0] = 1

active_neutron = True

numberAbsorp = 0 # Nombre de neutrons absorbés ou qui sont sortie du mur
numberPointsOutside = 0 # Nombre de neutrons qui sont derrière le mur
numberPointsBackScatter = 0 # Nombre de neutrons qui sont devant le mur


distances_absorp = []  # Pour stocker les distances avant absorption
distances_scatter = []  # Pour stocker les distances avant diffusion

for i in range(numberPoints):
    active_neutron = True
    while active_neutron:
        ethaAbsorp = np.random.uniform(0, 1)
        ethaScatter = np.random.uniform(0, 1)
    
        sampleAbsorp = -np.log(ethaAbsorp) / crossSectionAbsorp
        sampleScatter = -np.log(ethaScatter) / crossSectionScatter

        if pos[i, 0] > thicknessWall:
            numberPointsOutside += 1
            active_neutron = False
            break

        if pos[i, 0] < 0:
            numberPointsBackScatter += 1
            active_neutron = False
            break
        
        if sampleAbsorp < sampleScatter:
            pos[i, :] += sampleAbsorp * direction[i, :]
            active_neutron = False
            distances_absorp.append(sampleAbsorp)  # Enregistre la distance avant absorption
            numberAbsorp += 1
            break
        
        else:
            pos[i, :] += sampleScatter * direction[i, :]
            theta = np.random.uniform(0, 2 * np.pi)
            direction[i, :] = [np.cos(theta), np.sin(theta)]
            distances_scatter.append(sampleScatter)  # Enregistre la distance avant diffusion
    printProgressBar(i, numberPoints, prefix='Progress:', suffix='Complete', decimals = 3,length=50)

print('Number of points: ', numberPoints)
print('Number of points outside: ', numberPointsOutside)
print('Number of points backscattered: ', numberPointsBackScatter)
print('Distance before absorption: ', np.mean(distances_absorp))
print('Distance before scattering: ', np.mean(distances_scatter))

x_limits = (thicknessWall - thicknessWall*1.5, thicknessWall*1.5)
y_limits = (-thicknessWall*1.5, thicknessWall*1.5)
#x_limits = (0, thicknessWall)
#y_limits = (-thicknessWall, thicknessWall)


plt.hist2d(pos[:, 0], pos[:, 1], bins=100, range=[x_limits, y_limits], cmap='viridis', norm=LogNorm())
plt.colorbar(label='Densité des points')


plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Début de la région')
plt.axvline(x=thicknessWall, color='red', linestyle='--', linewidth=2, label='Fin de la région')

plt.xlabel('Position en X')
plt.ylabel('Position en Y')
plt.title(f'Nombre de points: {numberPoints}, \n'
          f'Nombre de points derrière le mur: {numberPointsOutside}, \n'
          f'Nombre de points devant le mur: {numberPointsBackScatter}')
plt.show()
