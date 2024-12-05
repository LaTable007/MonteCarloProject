import random

from CommonFunctions import InitNeutronPop, collisionSample, TransportSampling, ProbabilityTransmission
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
    if ethaTransport < SigmaSlim or len(wallData) - 1 == layer:
        S = ethaTransport/(wallData[layer][0] + wallData[layer][1])
    else :
        S = (wallData[layer][3] - pos[0]) / direction[0]
        SigmaS = (wallData[layer][0] + wallData[layer][1])*(wallData[layer][3] - pos[0])/direction[0]
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
            Si = (ethaTransport - SigmaS)/(wallData[-1][0] + wallData[-1][1])
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






def ProbabilityHeterogeneousTransmission(thicknessWall,  numberPoints, wallData):
    finalpos = []
    pos, direction, weight, splitted = InitNeutronPop(numberPoints, False)
    numberPointsBackScattered = 0
    numberPointsTransmitted = 0
    cycle = 0

    while len(pos) != 0:
        cycle += 1
        # stockage neutrons qui subissent un nouveau cycle :
        npos, ndirection, nsplitted, nweight = [], [], [], []


        for i in range(len(pos)):
            # echantillonage du transport kernel
            ethaTransport = random.uniform(0, 1)

            if direction[i][0] > 0:
                #print("Direction : " + str(direction[i][0]))
                TransportSample = TransportPositiveSampling(pos[i], direction[i], wallData, ethaTransport)


            else :
                #print("Direction : " + str(direction[i][0]))
                TransportSample = TransportNegativeSampling(pos[i], direction[i], wallData, ethaTransport)


            posix = pos[i][0]


            pos[i][0] += TransportSample *direction[i][0]




            # On verifie si neutron sort du mur
            if pos[i][0] < 0:
                finalpos.append(pos[i])
                numberPointsBackScattered += 1

            elif pos[i][0] >= thicknessWall:
                finalpos.append(pos[i])
                numberPointsTransmitted += 1

            else :
                # échantillonage du collision kernel
                layer = FindLayer(pos[i], wallData)
                scattering = collisionSample(wallData[layer][0],  wallData[layer][1])


                if scattering:
                    # détermination direction en sortie de la collision
                    theta = np.random.uniform(0, 2 * np.pi)
                    direction[i][0] = cos(theta)


                    #neutrons qui survivent à ce cycle et qui restent dans le mur
                    npos.append(pos[i])
                    ndirection.append(direction[i])
        pos = npos[:]
        direction = ndirection[:]
    return numberPointsTransmitted, numberPointsBackScattered, finalpos


thicknessWall = 0.15
numberPoints = 1000
wallData = [[67, 1, 0, 0.1], [67, 1, 0.1, thicknessWall]]



#pos = [0.05, 0]
#dir = [-1, 0]
#print(TransportNegativeSampling(pos, dir, wallData))

#SampleTransport = TransportSampling(wallData[0][0] + wallData[0][1], randompoint)
#pos[0] += SampleTransport*dir[0]
#print(pos[0])


HeterogeneousMeanValue = 0
HomogeneousMeanValue = 0
for j in range(100):
    print(j)
    numberPointsTransmitted, numberPointsBackScattered, finalpos = ProbabilityHeterogeneousTransmission(thicknessWall, numberPoints, wallData)
    NumberPointsTransmitted, NumberPointsBackScattered, Finalpos = ProbabilityTransmission(thicknessWall, wallData[0][1], wallData[0][0], numberPoints)
    HomogeneousMeanValue += NumberPointsTransmitted
    HeterogeneousMeanValue += numberPointsTransmitted

print("Heterogeneous method : " + str(HeterogeneousMeanValue/100))
print("Homogeneous method : " + str(HomogeneousMeanValue/100))
#print(numberPointsBackScattered)
#print(NumberPointsBackScattered)


#wall = [[1, 0.1, 0, 0.3],[1, 1, 0.3, 0.5], [1, 1, 0.5, 0.8]]

#print(FindLayer([0.2, 1], wall))
#print(FindLayer([0.4, 1], wall))
#print(FindLayer([0.6, 1], wall))