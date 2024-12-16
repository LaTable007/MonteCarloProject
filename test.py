from CommonFunctionsReliability import *
import numpy as np
import matplotlib.pyplot as plt


seed = 1
np.random.seed(seed)



Lambda_1 = 0.0001
Lambda = 0.0001
Mu = 0.0001
Mu_1 = 0.0001
Tmiss = 10000

Lambda_Primme = 0.001
Mu_Primme = 0.001
Lambda1_Primme = 0.001
Mu1_Primme = 0.001

A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]

A_Primme = [[-Lambda1_Primme, 0, 0, Lambda1_Primme, 0, 0], [Mu_Primme, -Mu_Primme - Lambda_Primme, 0, 0, Lambda1_Primme, 0],
     [0, 2 * Mu_Primme, -2 * Mu_Primme - Lambda1_Primme, 0, 0, Lambda1_Primme], [Mu1_Primme, 0, 0, -Mu1_Primme - Lambda_Primme, Lambda_Primme, 0],
     [0, 0, 0, Mu_Primme, -Mu_Primme - Lambda_Primme, Lambda_Primme], [0, 0, Mu1_Primme, 0, 2 * Mu_Primme, -Mu1_Primme - 2 * Mu_Primme]]


numberSimValues = np.linspace(1000, 10000, 51)
VarianceData = []
VarianceBiasData = []
VarianceBiasEventData = []
for numSim in numberSimValues:
    numberUnreliableStates, numberUnavailableStates = Unreliability(int(numSim), Tmiss, A)
    VarianceData.append(VarianceCalculation(int(numSim), numberUnreliableStates))
    NumberUnreliableStates, NumberUnavailableStates, UnreliableWeights, UnavailableWeights = UnreliabilityBias(int(numSim), Tmiss, A, A_Primme)
    NbrUnreliableStates, NbrUnavailableStates, UnreliableWghts, UnavailableWghts = UnreliabilityCompBias(int(numSim), Tmiss, A, A_Primme)
    VarianceBiasData.append(ErrorEstimation(UnavailableWeights, int(numSim), NumberUnreliableStates))
    VarianceBiasEventData.append(ErrorEstimation(UnreliableWghts, int(numSim), NbrUnreliableStates))
    print(numSim, numberUnreliableStates/numSim, NumberUnreliableStates/numSim, NbrUnreliableStates/numSim)

plt.figure(figsize=(10, 6))
plt.plot(numberSimValues, VarianceData, numberSimValues, VarianceBiasData, numberSimValues, VarianceBiasEventData)
plt.show()





























"""
a = 0
b = 0
c = 0
numberUnreliableStates, numberUnavailableStates = Unreliability(numberSim, Tmiss)
unreliability_list, unavailability_list, weights = UnreliabilityWithImportanceSampling(numberSim, Tmiss)
for i in unreliability_list :
    a += i/numberSim
for i in unavailability_list:
    b += i/numberSim
for i in weights:
    c += i
print(numberUnreliableStates/numberSim, numberUnavailableStates/numberSim)
numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights= UnreliabilityBias(numberSim, Tmiss)

print(a, b, c)
print(numberUnreliableStates/numberSim, numberUnavailableStates/numberSim)
"""