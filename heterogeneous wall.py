import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from utils import printProgressBar

# Constants

crossSectionAbsorp = 1  # Définition d'une valeur pour la cross Section d'absorption pas tenir compte des dimensions pour l'instant
crossSectionScatter = 67  # Même chose pour la cross Section de diffusion
numberPoints = 100000  # Nombre de neutrons envoyé
thicknessWall = 0.1  # Épaisseur de la paroi
totalCrossSection = crossSectionScatter + crossSectionAbsorp

pos = np.zeros((numberPoints, 2))  # Position initiale des neutrons
direction = np.zeros((numberPoints, 2))  # Direction initiale des neutrons
direction[:, 0] = 1

active_neutron = True

numberAbsorp = 0  # Nombre de neutrons absorbés ou qui sont sortie du mur
numberPointsOutside = 0  # Nombre de neutrons qui sont derrière le mur
numberPointsBackScatter = 0  # Nombre de neutrons qui sont devant le mur

distances_absorp = []  # Pour stocker les distances avant absorption
distances_scatter = []  # Pour stocker les distances avant diffusion

wallData = [[67, 1, 0, 0.05],[42,3 , 0.05, thicknessWall]]




def collisionSample(sigmaS, sigmaA):
    etha = random.uniform(0, 1)
    if etha < sigmaS/(sigmaA + sigmaS) : x = True
    else : x = False
    return x

for i in range(numberPoints):
    active_neutron = True
    while active_neutron:

        if pos[i, 0] > thicknessWall:
            numberPointsOutside += 1
            active_neutron = False
            break

        if pos[i, 0] < 0:
            numberPointsBackScatter += 1
            active_neutron = False
            break

        ethaTransport = random.uniform(0, 1)
        sampleTransport = -np.log(ethaTransport) / totalCrossSection

        pos[i, :] += sampleTransport*direction[i, :]

        for wall in wallData:
            if wall[2] <= pos[i, 0] < wall[3]:
                w = wallData.index(wall)
        scattering = collisionSample(crossSectionScatter, crossSectionAbsorp)


        if scattering :
            theta = np.random.uniform(0, 2 * np.pi)
            direction[i, :] = [np.cos(theta), np.sin(theta)]
            distances_scatter.append(sampleTransport)

        else :
            active_neutron = False
            distances_absorp.append(sampleTransport)  # Enregistre la distance avant absorption
            numberAbsorp += 1

    printProgressBar(i, numberPoints, prefix='Progress:', suffix='Complete', decimals=3, length=50)

print('Number of points: ', numberPoints)
print('Number of points outside: ', numberPointsOutside)
print('Number of points backscattered: ', numberPointsBackScatter)
print('Distance before absorption: ', np.mean(distances_absorp))
print('Distance before scattering: ', np.mean(distances_scatter))

x_limits = (thicknessWall - thicknessWall * 1.5, thicknessWall * 1.5)
y_limits = (-thicknessWall * 1.5, thicknessWall * 1.5)
# x_limits = (0, thicknessWall)
# y_limits = (-thicknessWall, thicknessWall)


plt.hist2d(pos[:, 0], pos[:, 1], bins=100, range=[x_limits, y_limits], cmap='viridis', norm=LogNorm())
plt.colorbar(label='Densité des points')
for wall in wallData:
    plt.axvline(x=wall[2], color='red', linestyle='--', linewidth=2, label='Début de la région')
plt.axvline(x=thicknessWall, color='red', linestyle='--', linewidth=2, label='Fin de la région')

plt.xlabel('Position en X')
plt.ylabel('Position en Y')
plt.title(f'Nombre de points: {numberPoints}, \n'
          f'Nombre de points derrière le mur: {numberPointsOutside}, \n'
          f'Nombre de points devant le mur: {numberPointsBackScatter}')
plt.show()
