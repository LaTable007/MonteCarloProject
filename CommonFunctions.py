import random
from math import log, cos, sin, exp
import numpy as np
import matplotlib.pyplot as plt




def TransportSampling(TotalCrossSection, randompoint):
    etha = random.uniform(0, 1)
    #return -log(etha)/TotalCrossSection
    return -np.log(randompoint)/TotalCrossSection

def collisionSample(sigmaS, sigmaA):
    etha = random.uniform(0, 1)
    if etha < sigmaS / (sigmaA + sigmaS):
        x = True
    else:
        x = False
    return x

def VarianceCalculation(TotalNumberNeutrons, TransmittedNeutrons):
    var = TransmittedNeutrons/TotalNumberNeutrons - (TransmittedNeutrons/TotalNumberNeutrons)**2
    return (var/TotalNumberNeutrons)**(1/2)


def InitNeutronPop(NumberNeutrons, split):
    weight = []
    splitted = []
    pos = [[0, 0] for _ in range(NumberNeutrons)]  # Position initiale des neutrons
    direction = [[1, 0] for _ in range(NumberNeutrons)]  # Direction initiale des neutrons
    if split:
        weight = [1 for _ in range(NumberNeutrons)]
        splitted = [False for _ in range(NumberNeutrons)]
    return pos, direction, weight, splitted


def ProbabilityTransmission(thicknessWall, AbsorpCrossSection, ScatteringCrossSection, numberPoints):
    finalpos = []
    pos, direction, weight, splitted = InitNeutronPop(numberPoints, False)
    numberPointsBackScattered = 0
    numberPointsTransmitted = 0

    while len(pos) != 0:
        # stockage neutrons qui subissent un nouveau cycle :
        npos, ndirection, nsplitted, nweight = [], [], [], []

        for i in range(len(pos)):
            # echantillonage du transport kernel
            randompoint = random.uniform(0, 1)
            SampleTransport = TransportSampling(AbsorpCrossSection + ScatteringCrossSection, randompoint)
            pos[i][0] += SampleTransport * direction[i][0]

            # On verifie si neutron sort du mur
            if pos[i][0] < 0:
                finalpos.append(pos[i])
                numberPointsBackScattered += 1

            elif pos[i][0] >= thicknessWall:
                finalpos.append(pos[i])
                numberPointsTransmitted += 1

            else :
                # échantillonage du collision kernel
                scattering = collisionSample(ScatteringCrossSection, AbsorpCrossSection)


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
