import random

import numpy as np
from math import cos
from CommonFunctions import InitNeutronPop, TransportSampling, collisionSample, ProbabilityTransmission, VarianceCalculation, RussianRoulette
import matplotlib.pyplot as plt



def ProbabilitySplittingTransmission(thicknessWall, AbsorpCrossSection, ScatteringCrossSection, numberPoints, near_boundary_margin, WeightThreshold, split_factor):
    finalweight = []
    pos, direction, weight, splitted = InitNeutronPop(numberPoints, True)

    numberPointsBackScattered = 0
    numberPointsTransmitted = 0
    numberPointsAbsorbed = 0

    while len(pos) != 0:
        # stockage neutrons qui subissent un nouveau cycle :
        npos, ndirection, nweight = [], [], []

        for i in range(len(pos)):
            # execution de la russian roulette
            Killed, weight[i] = RussianRoulette(weight[i], WeightThreshold)

            # échantillonage du transport kernel
            SampleTransport = TransportSampling(AbsorpCrossSection + ScatteringCrossSection)
            pos[i][0] += SampleTransport * direction[i][0]
            if not Killed :

                # On verifie si neutron sort du mur
                if pos[i][0] < 0:
                    numberPointsBackScattered += weight[i]

                elif pos[i][0] >= thicknessWall:
                    finalweight.append(weight[i])
                    numberPointsTransmitted += weight[i]

                else :
                    # échantillonage du collision kernel
                    justsplitted = False
                    scattering = collisionSample(ScatteringCrossSection, AbsorpCrossSection)
                    if scattering:
                        # détermination direction en sortie de la collision

                        theta = np.random.uniform(0, 2 * np.pi)
                        direction[i][0] = cos(theta)

                    else:
                        #compte le nombre de neutrons absorbés dans le mur
                        numberPointsAbsorbed += weight[i]
                    #On détermine si un neutron doit être splitté
                    if pos[i][0] >= thicknessWall - near_boundary_margin and scattering:

                        justsplitted = True   # Élimine le neutron qu'on va splitter

                        #On crée les splitted neutrons et on les ajoute au prochain cycle
                        for _ in range(split_factor):
                            npos.append([pos[i][0], pos[i][1]])
                            ndirection.append([direction[i][0], direction[i][1]])
                            nweight.append(weight[i] / split_factor) #le poids du neutron au compteur est réduit par le nombre de neutrons créés


                    if not justsplitted and scattering:
                        # neutrons qui survivent à ce cycle et qui restent dans le mur
                        npos.append(pos[i])
                        ndirection.append(direction[i])
                        nweight.append(weight[i])

        pos = npos[:]
        direction = ndirection[:]
        weight = nweight[:]
    return numberPointsTransmitted, finalweight


def ErrorEstimation(ScatteredWeights, numberPoints, numberPointsTransmitted):
    var = 0
    for weight in ScatteredWeights:
        var += weight**2

    var = var/numberPoints - (numberPointsTransmitted/numberPoints)**2
    return (var/numberPoints)**(1/2)

"""
#numberPoints = 10000
ThicknessWall = 50
ACrossSection = 0.02
SCrossSection = 0.60
VarianceData = []
SplittedErrorData = []
WeightThreshold = 0.001
WeightThresholdData = []
Abs = []

#NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,SCrossSection, numberPoints)
#print(NbPtsTransmitted/numberPoints)

numberPoints = 100000
for i in range(50):
    numberPoints += 10000
    NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,
                                                                                  SCrossSection, numberPoints)
    print(NbPtsTransmitted/numberPoints)
    numberPointsTransmitted, ScatteredWeights = ProbabilitySplittingTransmission(ThicknessWall, ACrossSection, SCrossSection, numberPoints, 1.5, 0.01, 50)
    vars = ErrorEstimation(ScatteredWeights, numberPoints, numberPointsTransmitted)
    var = VarianceCalculation(numberPoints, NbPtsTransmitted)
    SplittedErrorData.append(vars)
    VarianceData.append(var)

label = ["Analog", "Splitting and RR"]
fig, ax0 = plt.subplots(1, 1)
ax0.plot([100 * (i + 1) for i in range(50)], VarianceData, label= "Analog MC")
ax0.plot( [100 * (i + 1) for i in range(50)], SplittedErrorData, label= "Splitting and RR MC")
ax0.legend()
plt.show()
"""

















