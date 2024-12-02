import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm 
from utils import printProgressBar


# Constants
seed = 1
np.random.seed(seed)

crossSectionAbsorp = 1 # Définition d'une valeur pour la cross Section d'absorption
crossSectionScatter = 67 # Même chose pour la diffusion
numberPoints = 100000 # Nombre de neutrons envoyé
thicknessWall = 0.2 # Épaisseur de la paroi
totalCrossSection = crossSectionScatter + crossSectionAbsorp

pos = np.zeros((numberPoints, 2)) # Position initiale des neutrons
direction = np.zeros((numberPoints, 2)) # Direction initiale des neutrons
direction[:, 0] = 1

numberAbsorp = 0 # Nombre de neutrons absorbés ou qui sont sortie du mur
numberPointsOutside = 0 # Nombre de neutrons qui sont derrière le mur
numberPointsBackScatter = 0 # Nombre de neutrons qui sont devant le mur


distances_absorp = []  # Pour stocker les distances avant absorption
distances_scatter = []  # Pour stocker les distances avant diffusion

neutron_population = np.zeros(numberPoints)
j = 0

def collisionSample(sigmaS, sigmaA):
    etha1 = np.random.uniform(0, 1)
    #etha2 = 1 - etha1 
    etha2 = np.random.uniform(0, 1)
    x = [False, False]
    if etha1 < sigmaS/(sigmaA + sigmaS) : x[0] = True
    else : x[0] = False
    if etha2 < sigmaS/(sigmaA + sigmaS) : x[1] = True
    else : x[1] = False
    return x

for i in range(0, numberPoints, 2):
    active_neutron_pair = [True, True]
    while active_neutron_pair[0] or active_neutron_pair[1]:

        if active_neutron_pair[0]:
            if pos[i, 0] > thicknessWall:
                numberPointsOutside += 1
                active_neutron_pair[0] = False
                neutron_population[j] = 1
                j += 1
                break

            if pos[i, 0] < 0:
                numberPointsBackScatter += 1
                active_neutron_pair[0] = False
                neutron_population[j] = 0
                j += 1
                break 

        if active_neutron_pair[1]:
            if pos[i+1, 0] > thicknessWall:
                numberPointsOutside += 1
                active_neutron_pair[1] = False
                neutron_population[j] = 1
                j += 1
                break

            if pos[i+1, 0] < 0:
                numberPointsBackScatter += 1
                active_neutron_pair[1] = False
                neutron_population[j] = 0
                j += 1
                break
        
        ethaTransport = np.random.uniform(0, 1, 2)
        ethaTransport[1] = 1 - ethaTransport[0]

        sampleTransport = -np.log(ethaTransport) / (totalCrossSection)

        pos[i, :] += sampleTransport[0]*direction[i, :]
        pos[i+1, :] += sampleTransport[1]*direction[i+1, :]

        scattering = collisionSample(crossSectionScatter, crossSectionAbsorp)

        if active_neutron_pair[0]:
            if scattering[0]:
                theta = np.random.uniform(0, 2 * np.pi)
                direction[i, :] = [np.cos(theta), np.sin(theta)]
                distances_scatter.append(sampleTransport[0])

            else:
                active_neutron_pair[0] = False
                distances_absorp.append(sampleTransport[0])
                neutron_population[j] = 0
                j += 1

        if active_neutron_pair[1]:
            if scattering[1]:
                theta = np.random.uniform(0, 2 * np.pi)
                direction[i+1, :] = [np.cos(theta), np.sin(theta)]
                distances_scatter.append(sampleTransport[1])

            else:
                active_neutron_pair[1] = False
                distances_absorp.append(sampleTransport[1])
                neutron_population[j] = 0
                j += 1
           
    printProgressBar(i, numberPoints, prefix='Progress:', suffix='Complete', decimals = 3,length=50)

# Calculate the standard deviation of the x position

stdX = np.std(neutron_population)

print('Number of points: ', numberPoints)
print('Number of points outside: ', numberPointsOutside)
print('Number of points backscattered: ', numberPointsBackScatter)
print('Distance before absorption: ', np.mean(distances_absorp))
print('Distance before scattering: ', np.mean(distances_scatter))

print('Standard deviation of the neutron population: ', stdX)

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
