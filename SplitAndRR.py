import random

import numpy as np
from math import cos
from CommonFunctions import InitNeutronPop, TransportSampling, collisionSample, ProbabilityTransmission, VarianceCalculation
import matplotlib.pyplot as plt


def ProbabilitySplittingTransmission(thicknessWall, AbsorpCrossSection, ScatteringCrossSection, numberPoints, near_boundary_margin):
    finalpos = []
    finalweight = []
    pos, direction, weight, splitted = InitNeutronPop(numberPoints, True)
    WeightThreshold = 0.09
    numberPointsBackScattered = 0
    numberPointsTransmitted = 0
    numberPointsAbsorbed = 0
    numberSplits = 0
    split_factor = 10

    while len(pos) != 0:
        # stockage neutrons qui subissent un nouveau cycle :
        npos, ndirection, nsplitted, nweight = [], [], [], []

        for i in range(len(pos)):
            # echantillonage du transport kernel
            Killed = False
            if weight[i] <= WeightThreshold:
                ethaThreshold = random.uniform(0, 1)
                if ethaThreshold <= WeightThreshold:
                    weight[i] = weight[i]/WeightThreshold
                else : Killed = True

            SampleTransport = TransportSampling(AbsorpCrossSection + ScatteringCrossSection)
            pos[i][0] += SampleTransport * direction[i][0]
            if not Killed :

                # On verifie si neutron sort du mur
                if pos[i][0] < 0:
                    numberPointsBackScattered += weight[i]

                elif pos[i][0] >= thicknessWall:
                    finalpos.append(pos[i])
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

                        numberSplits += 1
                        justsplitted = True   # Élimine le neutron qu'on va splitter

                        #On crée les splitted neutrons et on les ajoute au prochain cycle
                        for _ in range(split_factor):
                            npos.append([pos[i][0], pos[i][1]])
                            ndirection.append([direction[i][0], direction[i][1]])
                            nsplitted.append(True)
                            nweight.append(weight[i] / split_factor) #le poids du neutron au compteur est réduit par le nombre de neutrons créés


                    if not justsplitted and scattering:
                        # neutrons qui survivent à ce cycle et qui restent dans le mur
                        npos.append(pos[i])
                        ndirection.append(direction[i])
                        nsplitted.append(splitted[i])
                        nweight.append(weight[i])

        pos = npos[:]
        direction = ndirection[:]
        weight = nweight[:]
        splitted = nsplitted[:]
    return numberPointsTransmitted, finalpos, finalweight


def ErrorEstimation(ScatteredWeights, numberPoints, numberPointsTransmitted):
    var = 0
    for weight in ScatteredWeights:
        var += weight**2

    var = var/numberPoints - (numberPointsTransmitted/numberPoints)**2
    return (var/numberPoints)**(1/2)


numberPoints = 0
ThicknessWall = 0.1
ACrossSection = 1
SCrossSection = 67
VarianceData = []
SplittedErrorData = []


for i in range(50):
    numberPoints += 100
    NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,
                                                                                  SCrossSection, numberPoints)
    numberPointsTransmitted, ScatteredPos, ScatteredWeights = ProbabilitySplittingTransmission(ThicknessWall, ACrossSection, SCrossSection, numberPoints, 0.01)
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








