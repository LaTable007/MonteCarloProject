import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm 
from utils import printProgressBar


# Constants

crossSectionAbsorp = 1 # Définition d'une valeur pour la cross Section d'absorption pas tenir compte des dimensions pour l'instant 
crossSectionScatter = 67 # Même chose pour la cross Section de diffusion
numberPoints = 10000000 # Nombre de neutrons envoyé
thicknessWall = 0.2 # Épaisseur de la paroi

pos = np.zeros((numberPoints, 2)) # Position initiale des neutrons
direction = np.zeros((numberPoints, 2)) # Direction initiale des neutrons
direction[:, 0] = 1

active_neutron = np.ones(numberPoints, dtype=bool)

numberAbsorp = 0 # Nombre de neutrons absorbés ou qui sont sortie du mur
numberPointsOutside = 0 # Nombre de neutrons qui sont derrière le mur
numberPointsBackScatter = 0 # Nombre de neutrons qui sont devant le mur


distances_absorp = []  # Pour stocker les distances avant absorption
distances_scatter = []  # Pour stocker les distances avant diffusion


while active_neutron.any():
    # Obtenir les indices des neutrons actifs
    active_indices = np.where(active_neutron)[0]
    
    # Extraire les positions et directions des neutrons actifs
    pos_active = pos[active_indices]
    direction_active = direction[active_indices]

    # Génération des distances pour absorption et diffusion pour les neutrons actifs
    ethaAbsorp_active = np.random.uniform(0, 1, pos_active.shape[0])
    ethaScatter_active = np.random.uniform(0, 1, pos_active.shape[0])
    sampleAbsorp = -np.log(ethaAbsorp_active) / crossSectionAbsorp
    sampleScatter = -np.log(ethaScatter_active) / crossSectionScatter

    # Déterminer le sort des neutrons
    absorbed = sampleAbsorp < sampleScatter
    pos_active[absorbed] += sampleAbsorp[absorbed, np.newaxis] * direction_active[absorbed]

    # Mettre à jour les neutrons absorbés
    absorbed_indices = active_indices[absorbed]
    active_neutron[absorbed_indices] = False  # Marquer les neutrons absorbés comme inactifs

    # Pour les neutrons diffusés (non absorbés)
    scattered = ~absorbed
    pos_active[scattered] += sampleScatter[scattered, np.newaxis] * direction_active[scattered]
    theta = np.random.uniform(0, 2 * np.pi, scattered.sum())
    direction_active[scattered] = np.column_stack((np.cos(theta), np.sin(theta)))

    # Mise à jour des positions et directions pour les neutrons actifs
    pos[active_indices] = pos_active
    direction[active_indices] = direction_active

    # Détecter les neutrons en dehors des limites du mur
    beyond_wall = pos_active[:, 0] > thicknessWall
    behind_wall = pos_active[:, 0] < 0

    # Mettre à jour les neutrons en dehors du mur comme inactifs
    outside_indices = active_indices[beyond_wall | behind_wall]
    active_neutron[outside_indices] = False

"""
print('Number of points: ', numberPoints)
print('Number of points outside: ', numberPointsOutside)
print('Number of points backscattered: ', numberPointsBackScatter)
print('Distance before absorption: ', np.mean(distances_absorp))
print('Distance before scattering: ', np.mean(distances_scatter))
"""


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
#plt.title(f'Nombre de points: {numberPoints}, \n' f'Nombre de points derrière le mur: {numberPointsOutside}, \n' f'Nombre de points devant le mur: {numberPointsBackScatter}')
plt.show()
