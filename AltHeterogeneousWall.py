import random

from CommonFunctions import InitNeutronPop, collisionSample, TransportSampling, ProbabilityTransmission, RussianRoulette
from HeterogeneousWall import ProbabilityHeterogeneousTransmission, FindLayer, AltTransportSampling
import numpy as np
from math import cos






def ProbabilityAltHeterogeneousTransmission(thicknessWall,  numberPoints, wallData, WeightThreshold, near_boundary_margin, split_factor):
    finalweight = []
    pos, direction, weight, splitted = InitNeutronPop(numberPoints, True)
    numberPointsBackScattered = 0
    numberPointsTransmitted = 0
    numberPointsAbsorbed = 0

    while len(pos) != 0:
        # stockage neutrons qui subissent un nouveau cycle :
        npos, ndirection, nweight = [], [], []

        for i in range(len(pos)):

            Killed = False

            if WeightThreshold != 0 :Killed, weight[i] = RussianRoulette(weight[i], WeightThreshold)

            # echantillonage du transport kernel
            randompoint = random.uniform(0, 1)

            pos[i][0] = AltTransportSampling(pos[i], direction[i], wallData, randompoint)

            if not Killed:

                # On verifie si neutron sort du mur
                if pos[i][0] < 0:
                    numberPointsBackScattered += weight[i]

                elif pos[i][0] >= thicknessWall:
                    finalweight.append(weight[i])
                    numberPointsTransmitted += weight[i]

                else :
                    # échantillonage du collision kernel
                    justsplitted = False
                    layer = FindLayer(pos[i], wallData)
                    scattering = collisionSample(wallData[layer][0],  wallData[layer][1])


                    if scattering:
                        # détermination direction en sortie de la collision
                        theta = np.random.uniform(0, 2 * np.pi)
                        direction[i][0] = cos(theta)


                    else :
                        numberPointsAbsorbed += weight[i]

                    if pos[i][0] >= thicknessWall - near_boundary_margin and scattering and split_factor > 1:

                        justsplitted = True   # Élimine le neutron qu'on va splitter


                        #vérifie s'il y a du splitting
                            #creation des neutrons splittés
                        for _ in range(split_factor):
                            npos.append([pos[i][0], pos[i][1]])
                            ndirection.append([direction[i][0], direction[i][1]])
                            nweight.append(weight[i] / split_factor) #le poids du neutron au compteur est réduit par le nombre de neutrons créés

                    if not justsplitted and scattering:
                        # neutrons qui survivent à ce cycle et qui restent dans le mur
                        npos.append(pos[i])
                        ndirection.append(direction[i])
                        nweight.append(weight[i])

        weight = nweight[:]
        pos = npos[:]
        direction = ndirection[:]
    return numberPointsTransmitted, numberPointsBackScattered, finalweight
thicknessWall = 0.2
wallData = [[67, 1, 0, 0.1],[42, 3, 0.1, thicknessWall]]
WeightThreshold = 0
near_boundary_margin = 0
split_factor = 0
numberPoints = 1000
a = 0
b = 0

for i in range(100):
    print(i)
    numberPointsTransmitted, numberPointsBackScattered, finalweight = ProbabilityHeterogeneousTransmission(thicknessWall,  numberPoints, wallData, WeightThreshold, near_boundary_margin, split_factor)
#    print(numberPointsTransmitted/numberPoints)
    a += numberPointsTransmitted/(100*numberPoints)
    numberPointsTransmitted, numberPointsBackScattered, finalweight = ProbabilityAltHeterogeneousTransmission(thicknessWall,  numberPoints, wallData, WeightThreshold, near_boundary_margin, split_factor)
#    print(numberPointsTransmitted/numberPoints)
    b += numberPointsTransmitted/(100*numberPoints)

print(a)
print(b)






