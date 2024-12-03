import random
from math import log, cos, sin, exp
import numpy as np
from CommonFunctions import InitNeutronPop, TransportSampling, collisionSample, ProbabilityTransmission, VarianceCalculation

def ErrorEstimation(ScatteredWeights, numberPoints, numberPointsTransmitted):
    var = 0
    for weight in ScatteredWeights:
        var += weight**2

    var = var/numberPoints - (numberPointsTransmitted/numberPoints)**2
    return (var/numberPoints)**(1/2)


def ProbabilityATransmission(thicknessWall, AbsorpCrossSection, ScatteringCrossSection, numberPoints):
    finalpos = []
    finalweight = []
    pos, direction, weight, splitted = InitNeutronPop(numberPoints, True)
    numberPointsBackScattered = 0
    numberPointsTransmitted = 0
    while len(pos) != 0:
        # stockage neutrons qui subissent un nouveau cycle :
        npos, ndirection, nsplitted, nweight = [], [], [], []

        for i in range(len(pos)):
            if direction[i][0] > 0:
                Proba = exp(-(AbsorpCrossSection + ScatteringCrossSection)*(thicknessWall - pos[i][0])/direction[i][0])
                numberPointsTransmitted += Proba
                weight[i] *= 1 - Proba
                finalweight.append(Proba)
             #echantillonage du transport kernel
            SampleTransport = TransportSampling(AbsorpCrossSection + ScatteringCrossSection)
            pos[i][0] += SampleTransport * direction[i][0]

            # On verifie si neutron sort du mur
            if pos[i][0] < 0:
                finalpos.append(pos[i])
                numberPointsBackScattered += weight[i]

            elif pos[i][0] >= thicknessWall:
                finalpos.append(pos[i])
                finalweight.append(weight[i])
                #numberPointsTransmitted += weight[i]

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
                    nweight.append(weight[i])




        pos = npos[:]
        direction = ndirection[:]
        weight = nweight[:]
    return numberPointsTransmitted, numberPointsBackScattered,  finalweight


thicknessWall = 0.1
AbsorpCrossSection = 1
ScatteringCrossSection = 67
numberPoints = 10000
TotalnumberPointsTransmitted = 0
totalnumberPointsTransmitted = 0

NumberPointsTransmitted, NumberPointsBackScattered, Finalweight = ProbabilityTransmission(thicknessWall, AbsorpCrossSection, ScatteringCrossSection, numberPoints)
numberPointsTransmitted, numberPointsBackScattered, finalweight = ProbabilityATransmission(thicknessWall, AbsorpCrossSection, ScatteringCrossSection, numberPoints)

var1 = ErrorEstimation(finalweight,  numberPoints, numberPointsTransmitted)
var2 = VarianceCalculation(numberPoints, NumberPointsTransmitted)
print(var1)
print(var2)








