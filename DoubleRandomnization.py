import numpy as np
from HeterogeneousWall import FindLayer
from CommonFunctions import InitNeutronPop, collisionSample, TransportSampling, RussianRoulette
import random
from math import cos

MaxDeviation = 20

def meanValue(pos, wallData, Interaction):
    layer = FindLayer(pos, wallData)
    return wallData[layer][Interaction]

def StandardDeviation(pos, wallData):
    layer = FindLayer(pos, wallData)
    if pos[0] > (wallData[layer][2] + wallData[layer][3])/2:
        a = 2 * MaxDeviation/(wallData[layer][3] - wallData[layer][2])
        b = - MaxDeviation * (wallData[layer][3] + wallData[layer][2]) / (wallData[layer][3] - wallData[layer][2])
        sigma = a*pos[0] + b
    else :
        print("AAAAA")
        a =  2 * MaxDeviation /(wallData[layer][2] - wallData[layer][3])
        b = MaxDeviation * (wallData[layer][3] + wallData[layer][2]) / (wallData[layer][3] - wallData[layer][2])
        sigma = a * pos[0] + b
    return sigma






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

            pos[i][0] = RandomTransportSampling(pos[i], direction[i], wallData, randompoint)

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
                    #layer = FindLayer(pos[i], wallData)
                    AbsCrossSection, ScattCrossSection = ScattAndCaptCrossSection(pos[i], wallData)
                    scattering = collisionSample(ScattCrossSection,  AbsCrossSection)


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


def RandomTransportSampling(pos, dir, wallData, randompoint):
    layer0 = FindLayer(pos, wallData)
    layer1 = -1
    p0 = [pos[0], pos[1]]
    p1 = [pos[0], pos[1]]
    ethaTransport = -np.log(randompoint)
    while layer0 != layer1:
        TotCrossSection = TotalCrossSection(p0, wallData)
        TransportSample = ethaTransport/(TotCrossSection)
        p1[0] = p0[0] + TransportSample * dir[0]
        if layer0 != len(wallData) - 1:
            layer1 = FindLayer(p1, wallData)
        else : layer1 = layer0
        if layer0 != layer1 and layer0 != len(wallData) - 1:
            p1[0] = wallData[layer1][2]
            S = (p1[0] - p0[0])/dir[0]
            p0[0] = p1[0]
            ethaTransport -= (wallData[layer0][0] + wallData[layer0][1])*S
            layer0 = layer1
            layer1 = -1

    return p1[0]

def TotalCrossSection(pos, wallData):
    muS= meanValue(pos, wallData, 0)
    muC = meanValue(pos, wallData, 1)
    sigma = StandardDeviation(pos, wallData)
    return np.random.normal(muC + muS, 2**(1/2)*sigma)

def ScattAndCaptCrossSection(pos, wallData):
    muS= meanValue(pos, wallData, 0)
    muC = meanValue(pos, wallData, 1)
    sigma = StandardDeviation(pos, wallData)
    return np.random.normal(muC,sigma), np.random.normal(muS,sigma)








wallData = [[67, 1, 0, 0.1]]
pos = [0.05, 0]

sigma = StandardDeviation(pos, wallData)
mu = meanValue(pos, wallData, 0)
etha = np.random.normal(mu, sigma)
print(etha)


