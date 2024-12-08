import random

from CommonFunctions import InitNeutronPop, collisionSample, TransportSampling, ProbabilityTransmission, RussianRoulette
import numpy as np
from math import cos


def FindLayer(pos, wallData):
    layer = 0
    for i in range(len(wallData)):
        if wallData[i][2] <= pos[0] < wallData[i][3]:
            layer = i
            break
    return layer


def TransportPositiveSampling(pos, direction,  wallData, randompoint):
    ethaTransport = -np.log(randompoint)
    layer = FindLayer(pos, wallData)
    SigmaSlim = (wallData[layer][0] + wallData[layer][1])*(wallData[layer][3] - pos[0])/direction[0]
    a = np.exp(-SigmaSlim)
    if ethaTransport < SigmaSlim or len(wallData) - 1 == layer:
        S = ethaTransport/(wallData[layer][0] + wallData[layer][1])
    else :

        S = (wallData[layer][3] - pos[0]) / direction[0]
        #print(S)
        #print((wallData[layer][0] + wallData[layer][1]) * S)
        SigmaS = (wallData[layer][0] + wallData[layer][1])*S
        SampleEnded = False
        for i in range(layer + 1, len(wallData) - 1):
            SiMax = (wallData[i][3] - wallData[i][2]) / direction[0]
            SigmaSlim += (wallData[i][0] + wallData[i][1])*(wallData[i][3] - wallData[i][2])/direction[0]
            if ethaTransport < SigmaSlim:
                Si = (ethaTransport - SigmaS)/(wallData[i][0] + wallData[i][1])
                SampleEnded = True
                S += Si
                break
            else :
                SigmaS = SigmaSlim
                S += SiMax
        if not SampleEnded :
            #print("AAAAAA")
            Si = (ethaTransport - SigmaS)/(wallData[-1][0] + wallData[-1][1])
            b = np.exp(-(ethaTransport - SigmaS))
            S += Si
    return S

def TransportNegativeSampling(pos, direction, wallData, randompoint):
    ethaTransport = -np.log(randompoint)
    layer = FindLayer(pos, wallData)
    Smax = (wallData[layer][2] - pos[0]) / direction[0]
    SigmaSlim = (wallData[layer][0] + wallData[layer][1])*Smax
    if ethaTransport < SigmaSlim or  layer == 0:
        S = ethaTransport / (wallData[layer][0] + wallData[layer][1])
    else :
        SampleEndend = False
        S = Smax
        SigmaS = SigmaSlim
        for i in range(layer - 1, 0):
            SiMax = (wallData[i][2] - wallData[i][3])/direction[0]
            SigmaSlim += (wallData[i][0] + wallData[i][1])*SiMax
            if ethaTransport < SigmaSlim:
                SampleEndend = True
                Si = (ethaTransport - SigmaS)/(wallData[i][0]+ wallData[i][1])
                S += Si
                break
            else :
                SigmaS = SigmaSlim
                S += SiMax
        if not SampleEndend:
            Si = (ethaTransport - SigmaS)/(wallData[0][0]+ wallData[0][1])
            S += Si
    return S





def ProbabilityHeterogeneousTransmission(thicknessWall,  numberPoints, wallData, WeightThreshold, near_boundary_margin, split_factor):
    finalweight = []
    pos, direction, weight, splitted = InitNeutronPop(numberPoints, True)
    numberPointsBackScattered = 0
    numberPointsTransmitted = 0
    numberPointsAbsorbed = 0
    notEqual = 0
    total = 0



    while len(pos) != 0:
        # stockage neutrons qui subissent un nouveau cycle :
        npos, ndirection, nweight = [], [], []

        for i in range(len(pos)):
            total += 1
            Killed = False

            if WeightThreshold != 0 :Killed, weight[i] = RussianRoulette(weight[i], WeightThreshold)

            # echantillonage du transport kernel
            ethaTransport = random.uniform(0, 1)

            if direction[i][0] > 0:
                #print("Direction : " + str(direction[i][0]))
                TransportSample = TransportPositiveSampling(pos[i], direction[i], wallData, ethaTransport)
            else :
                #print("Direction : " + str(direction[i][0]))
                TransportSample = TransportNegativeSampling(pos[i], direction[i], wallData, ethaTransport)
            #layer = FindLayer(pos[i], wallData)
            #if(-np.log(ethaTransport) /(wallData[layer][0] + wallData[layer][1]) - TransportSample) != 0:
            #    print(-np.log(ethaTransport) /(wallData[layer][0] + wallData[layer][1]) - TransportSample)
            p = AltTransportSampling(pos[i], direction[i], wallData, ethaTransport)
            #print(p)

            pos[i][0] += TransportSample *direction[i][0]
            #print(pos[i][0])

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
    #print(total)
    #print(notEqual)
    return numberPointsTransmitted, numberPointsBackScattered, finalweight


thicknessWall = 0.2
numberPoints = 1000
wallData = [[67, 1, 0, 0.1], [42, 3, 0.1, thicknessWall]]
WeightThreshold = 0.1
near_boundary_margin = thicknessWall/10
split_factor = 5



"""
HeterogeneousMeanValue = 0
HomogeneousMeanValue = 0
for j in range(100):
    print(j)
    numberPointsTransmitted, numberPointsBackScattered, finalweight = ProbabilityHeterogeneousTransmission(thicknessWall, numberPoints
                                                                                                           , wallData, WeightThreshold, near_boundary_margin, split_factor)
    NumberPointsTransmitted, NumberPointsBackScattered, FinalWeight= ProbabilityTransmission(thicknessWall, wallData[0][1], wallData[0][0], numberPoints)
    HomogeneousMeanValue += NumberPointsTransmitted
    HeterogeneousMeanValue += numberPointsTransmitted

print("Heterogeneous method : " + str(HeterogeneousMeanValue/100))
print("Homogeneous method : " + str(HomogeneousMeanValue/100))
#print(numberPointsBackScattered)
#print(NumberPointsBackScattered)


#Méthode alternative pour l'évaluation de la transmission dans un mur hétérogène :


probabilityTransmission = 1
wallThickness = [wallData[i][3] - wallData[i][2] for i in range(len(wallData))]

numberPointsTransmitted, numberPointsBackScattered, finalweight = ProbabilityHeterogeneousTransmission(thicknessWall, numberPoints
                                                                                                           , wallData, WeightThreshold, near_boundary_margin, split_factor)
"""

def AltTransportSampling(pos, dir, wallData, randompoint):
    layer0 = FindLayer(pos, wallData)
    layer1 = -1
    p0 = [pos[0], pos[1]]
    p1 = [pos[0], pos[1]]
    ethaTransport = -np.log(randompoint)
    n = 0
    while layer0 != layer1:
        #n += 1
        #print(n)
        TransportSample = ethaTransport/(wallData[layer0][0]+wallData[layer0][1])
        p1[0] = p0[0] + TransportSample * dir[0]
        #pos[0] += TransportSample * dir[0]
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



def AltSampling(pos, dir, wallData, randomPoint):
    layer0 = FindLayer(pos, wallData)
    layer1 = -1
    ethaTransport = -np.log(randomPoint)
    TransportSample = ethaTransport/(wallData[layer0][0]+wallData[layer0][1])
    p = pos[0]
    pos[0] += TransportSample * dir[0]
    layer1 = FindLayer(pos, wallData)
    if layer1 != layer0 :
        x = (wallData[layer1][2] - p)
        S = (wallData[layer1][2] - p)/dir[0]
        print(S)
        ethaTransport -= (wallData[layer0][0]+wallData[layer0][1])*S
        pos[0] = wallData[layer1][2]
        #ethaTransport = random.uniform(0, 1)
        TransportSample = ethaTransport / (wallData[layer1][0] + wallData[layer1][1])
        pos[0] += TransportSample*dir[0]
    return pos[0]



"""
pos = [0, 0]
dir = [1, 0]
randomPoint = 0.001
print(TransportPositiveSampling(pos, dir, wallData, randomPoint))
print(AltTransportSampling(pos, dir, wallData, randomPoint))
"""


numberPointsTransmitted, numberPointsBackScattered, finalweight = ProbabilityHeterogeneousTransmission(thicknessWall, numberPoints
                                                                                                           , wallData, WeightThreshold, near_boundary_margin, split_factor)





