import random
from math import log, cos, sin
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from utils import printProgressBar

# Constants

crossSectionAbsorp = 1  # Définition d'une valeur pour la cross Section d'absorption pas tenir compte des dimensions pour l'instant
crossSectionScatter = 67  # Même chose pour la cross Section de diffusion
numberPoints = 100000# Nombre de neutrons envoyé
thicknessWall = 0.1  # Épaisseur de la paroi
totalCrossSection = crossSectionScatter + crossSectionAbsorp


#splitting constants
near_boundary_margin = 0.05
split_factor = 2
numberSplits = 0


#neutron population initialization
pos = [[0, 0] for _ in range(numberPoints)]  # Position initiale des neutrons
direction = [[1, 0] for _ in range(numberPoints)] # Direction initiale des neutrons
weight = [1 for _ in range(numberPoints)]
splitted = [False for _ in range(numberPoints)]
finalpos = []
finalweight = []
VarianceData = []
MeanData = []




active_neutron = True

numberAbsorp = 0  # Nombre de neutrons absorbés ou qui sont sortie du mur
numberPointsOutside = 0  # Nombre de neutrons qui sont derrière le mur
numberPointsBackScatter = 0  # Nombre de neutrons qui sont devant le mur

distances_absorp = []  # Pour stocker les distances avant absorption
distances_scatter = []  # Pour stocker les distances avant diffusion

wallData = [[67, 1, 0, 0.05],[42,3 , 0.05, thicknessWall]]
xlayer = []
for layer in wallData:
    print(layer)
    xlayer += [layer[2]]
xlayer += [thicknessWall]

def FindLayer(pos):
    layer = 0
    for j in range(len(wallData)):
        if wallData[j][2] <= pos[0] < wallData[j][3]:
            layer = j
            break
    return layer

def PassedNeutrons():
    n = 0
    totalweight = 0
    for i in range(len(finalpos)):
        totalweight += finalweight[i]
        if finalpos[i][0] >= thicknessWall:
            n += finalweight[i]

    return totalweight, n

def Variance(NumberOfNeutrons, PassedNumberOfNeutrons):
    var = 0
    for i in range(len(finalweight)):
        if finalpos[i][0] >= thicknessWall:
            var += finalweight[i]**2
    var = var/NumberOfNeutrons - (PassedNumberOfNeutrons/NumberOfNeutrons)**2
    return var**1/2




def collisionSample(sigmaS, sigmaA):
    etha = random.uniform(0, 1)
    if etha < sigmaS/(sigmaA + sigmaS) : x = True
    else : x = False
    return x

while len(pos) != 0:
    npos = []
    ndirection = []
    nsplitted = []
    nweight = []
    for i in range(len(pos)):
        layer =  FindLayer(pos[i])
        ethaTransport = random.uniform(0, 1)
        sampleTransport = -log(ethaTransport) /(wallData[layer][0] + wallData[layer][1])
        print(sampleTransport)
        pos[i][0] += sampleTransport * direction[i][0]
        pos[i][1] +=  sampleTransport * direction[i][1]
        if pos[i][0] < 0 :
            numberPointsBackScatter += weight[i]
            finalpos.append(pos[i])
            finalweight.append(weight[i])

        elif pos[i][0] >= thicknessWall :
            numberPointsOutside += weight[i]
            finalpos.append(pos[i])
            finalweight.append(weight[i])
        else :
            justsplitted = False
            #print(pos[i][0], pos[i][0] >= thicknessWall - near_boundary_margin)
#            if pos[i][0] >= thicknessWall - near_boundary_margin and not splitted[i]:
#                numberSplits += 1
#                justsplitted = True
#                for _ in range(split_factor):
#                    npos.append([pos[i][0], pos[i][1]])
#                    ndirection.append([direction[i][0], direction[i][1]])
#                    nsplitted.append(True)
                    #print(weight[i]/split_factor)
#                    nweight.append(weight[i]/split_factor)

            layer = FindLayer(pos[i])
            scattering = collisionSample(wallData[layer][0], wallData[layer][1])
            if scattering and not justsplitted:
                theta = np.random.uniform(0, 2 * np.pi)
                direction[i] = [cos(theta), sin(theta)]
                npos.append(pos[i])
                ndirection.append(direction[i])
                nsplitted.append(splitted[i])
                nweight.append(weight[i])
            else :
                if not justsplitted :
                    numberAbsorp += weight[i]
                    finalpos.append(pos[i])
                    finalweight.append(weight[i])
    NumberOfNeutrons, PassedNumberOfNeutrons = PassedNeutrons()
    #print(NumberOfNeutrons)
    if NumberOfNeutrons != 0:
        MeanData.append([NumberOfNeutrons, PassedNumberOfNeutrons/NumberOfNeutrons])
        VarianceData.append([NumberOfNeutrons, Variance(NumberOfNeutrons, PassedNumberOfNeutrons)/NumberOfNeutrons**(1/2)])



    pos = npos
    direction = ndirection
    splitted = nsplitted
    weight = nweight

#print(numberPointsOutside + numberAbsorp + numberPointsBackScatter)
#print(numberSplits)
#print(len(finalpos))
print(VarianceData[-1])
#print(MeanData[-1])
#print(finalweight)



















"""
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
        layer = 0
        for j in range(len(wallData)):
            if wallData[j][2] <= pos[i, 0] < wallData[j][3]:
                layer = j
                break

        scattering = collisionSample(wallData[layer][0], wallData[layer][1])
        if scattering :
            theta = np.random.uniform(0, 2 * np.pi)
            direction[i, :] = [np.cos(theta), np.sin(theta)]
            distances_scatter.append(sampleTransport)

        else :
            active_neutron = False
            distances_absorp.append(sampleTransport)  # Enregistre la distance avant absorption
            numberAbsorp += 1

    printProgressBar(i, numberPoints, prefix='Progress:', suffix='Complete', decimals=3, length=50)
"""


print('Number of points: ', numberPoints)
print('Number of points outside: ', numberPointsOutside)
print('Number of points backscattered: ', numberPointsBackScatter)
#print('Distance before absorption: ', np.mean(distances_absorp))
#print('Distance before scattering: ', np.mean(distances_scatter))

x_limits = (thicknessWall - thicknessWall * 1.5, thicknessWall * 1.5)
y_limits = (-thicknessWall * 1.5, thicknessWall * 1.5)
# x_limits = (0, thicknessWall)
# y_limits = (-thicknessWall, thicknessWall)

plt.plot([var[0] for var in VarianceData], [var[1] for var in VarianceData])
#plt.hist2d([posx[0] for posx in finalpos], [posy[1] for posy in finalpos], bins=100, range=[x_limits, y_limits], cmap='viridis', norm=LogNorm())
#plt.colorbar(label='Densité des points')
#for wall in wallData:
#    plt.axvline(x=wall[2], color='red', linestyle='--', linewidth=2, label='Début de la région')
#plt.axvline(x=thicknessWall, color='red', linestyle='--', linewidth=2, label='Fin de la région')

#plt.xlabel('Position en X')
#plt.ylabel('Position en Y')
plt.title(f'Nombre de points: {numberPoints}, \n'
          f'Nombre de points derrière le mur: {numberPointsOutside}, \n'
          f'Nombre de points devant le mur: {numberPointsBackScatter}')
plt.show()

