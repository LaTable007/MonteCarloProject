import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm 
from utils import printProgressBar
import time

# Debut de l'execution
start_time = time.time()


# Constantes

crossSectionAbsorp = 1 # Définition d'une valeur pour la cross Section d'absorption
crossSectionScatter = 67 # Même chose pour la diffusion
numberPoints = 100000 # Nombre de neutrons envoyés
thicknessWall = 0.2 # Épaisseur de la paroi
energy_threshold = 0.05  # Seuil minimal pour la russian roulette
survival_probability = 0.5  # Probabilité de survivre à la roulette
near_boundary_margin = 0.002  # Epaisseur sur laquelle on split
split_factor = 2  # Nombre de neutrons crées à chaque splitting


pos = np.zeros((numberPoints, 2)) # Position initiale des neutrons
direction = np.zeros((numberPoints, 2)) # Direction initiale des neutrons
direction[:, 0] = 1

neutron_energy = np.ones(numberPoints)  # Energie initiale des neutrons
neutron_weight = np.ones(numberPoints)  # Poids initial des neutrons
active_neutron = True

numberAbsorp = 0 # Nombre de neutrons absorbés ou qui sont sortie du mur
numberPointsOutside = 0 # Nombre de neutrons qui sont derrière le mur
numberPointsBackScatter = 0 # Nombre de neutrons qui sont devant le mur
distances_absorp = []  # Pour stocker les distances avant absorption
distances_scatter = []  # Pour stocker les distances avant diffusion
neutron_population = np.zeros(numberPoints)
j = 0

for i in range(numberPoints):
    active_neutron = True
    while active_neutron:
        ethaAbsorp = np.random.uniform(0, 1)
        ethaScatter = np.random.uniform(0, 1)
    
        sampleAbsorp = -np.log(ethaAbsorp) / crossSectionAbsorp
        sampleScatter = -np.log(ethaScatter) / crossSectionScatter

        if pos[i, 0] > thicknessWall:
            numberPointsOutside += neutron_weight[i]
            active_neutron = False
            neutron_population[j] = 1
            j += 1
            break

        if pos[i, 0] < 0:
            numberPointsBackScatter += neutron_weight[i]
            active_neutron = False
            neutron_population[j] = 0
            j += 1
            break
        
        if sampleAbsorp < sampleScatter:
            pos[i, :] += sampleAbsorp * direction[i, :]
            active_neutron = False
            distances_absorp.append(sampleAbsorp)  # Enregistre la distance avant absorption
            numberAbsorp += neutron_weight[i]
            neutron_population[j] = 0
            j += 1
            break
        
        else:
            pos[i, :] += sampleScatter * direction[i, :]
            theta = np.random.uniform(0, 2 * np.pi)
            direction[i, :] = [np.cos(theta), np.sin(theta)]
            distances_scatter.append(sampleScatter)  # Enregistre la distance avant diffusion

            # Condition splitting proche des parois
            if (
                    0 <= pos[i, 0] <= near_boundary_margin or
                    thicknessWall - near_boundary_margin <= pos[i, 0] <= thicknessWall
            ):
                for _ in range(split_factor - 1):
                    # Creation de neutrons filles de poids réduit
                    pos = np.append(pos, [pos[i, :]], axis=0)
                    direction = np.append(direction, [direction[i, :]], axis=0)
                    neutron_energy = np.append(neutron_energy, [neutron_energy[i]])
                    neutron_weight = np.append(neutron_weight, [neutron_weight[i] / split_factor])
                neutron_weight[i] /= split_factor

            # Diminution de l'energie du neutron
            neutron_energy[i] *= 0.9  # Exemple: perte d'energie de 10%

            # Condition Russian roulette
            if neutron_energy[i] < energy_threshold:
                if np.random.uniform(0, 1) > survival_probability:
                    active_neutron = False  # Le neutron est "tué"
                else:
                    neutron_energy[i] /= survival_probability  # Adjust weight to maintain unbiased result
        printProgressBar(i, numberPoints, prefix='Progress:', suffix='Complete', decimals=3, length=50)
# Deviation standard de la population
stdX = np.std(neutron_population)
std_population = np.std(neutron_population)  # deviation standard
standard_error = std_population / np.sqrt(numberPoints)  # erreur standard


print('Number of points: ', numberPoints)
print('Number of points outside: ', numberPointsOutside)
print('Number of points backscattered: ', numberPointsBackScatter)
print('Distance before absorption: ', np.mean(distances_absorp))
print('Distance before scattering: ', np.mean(distances_scatter))

print('Standard deviation of the neutron population: ', stdX)
print(f"Standard Error of the estimation: {standard_error:.5f}")


#x_limits = (thicknessWall - thicknessWall*1.5, thicknessWall*1.5)
#y_limits = (-thicknessWall*1.5, thicknessWall*1.5)
x_limits = (0, thicknessWall)
y_limits = (-thicknessWall, thicknessWall)


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

# Fin de l'execution
end_time = time.time()

# Print du temps d'execution
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")