# On fait d'abord une partie unreliability ce sera plus simple dans un premier temp
# en system based-approach
from CommonFunctionsReliability import *
import numpy as np
import matplotlib.pyplot as plt

#seed = 1
#np.random.seed(seed)

Lambda_1 = 0.0001
Lambda = 0.0001
Mu = 0.0001
Mu_1 = 0.0001

Lambda_Primme = 0.0001
Mu_Primme = 0.0001
Lambda1_Primme = 0.0001
Mu1_Primme = 0.0001
Tmiss = 10000
numberSim = 10000

# 1 = operating, 0 = failed, 2 = stand-by
possible_states = [[1, 2, 2], [0, 1, 2], [0, 0, 1], [0, 0, 0], [1, 2, 0], [1, 0, 0]]
# on garde l'ordre dans choisi dans possible states pour donner un numero à chauqe état pour pouvoir les identifier dans le code
A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]
Tmiss = 0
Tmiss_values = [(i + 1)*100 for i in range(100)]
unreliabilityData = []
unavailabiltyData = []
unreliabilityFFData = []
unavailabiltyFFData = []
unreliabilityDataV = []
unavailabiltyDataV = []
unreliabilityFFDataV = []
unavailabiltyFFDataV = []

for j in range(100):
     Tmiss += 100
     print(Tmiss)
     numberUnreliableStates, numberUnavailableStates = Unreliability(numberSim, Tmiss, A)
     unreliabilityData.append(numberUnreliableStates/numberSim)
     unavailabiltyData.append(numberUnavailableStates/numberSim)
     unreliabilityDataV.append(VarianceCalculation(numberSim, numberUnreliableStates))
     unavailabiltyDataV.append(VarianceCalculation(numberSim, numberUnavailableStates))
     numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights = UnreliabilityFFSystemBased(numberSim, Tmiss, A)
     unreliabilityFFData.append(numberUnreliableStates / numberSim)
     unavailabiltyFFData.append(numberUnavailableStates / numberSim)
     unreliabilityFFDataV.append(ErrorEstimation(UnreliableWeights, numberSim,numberUnreliableStates))
     unavailabiltyFFDataV.append(ErrorEstimation(UnavailableWeights, numberSim,numberUnavailableStates))





# Création des plots
fig, (ax0, ax1) = plt.subplots(1, 2)
plt.figure(figsize=(10, 6))
ax0.set_title("Unreliability and unavailability vs Time")
ax0.plot(Tmiss_values, unreliabilityData, label="Unreliability")
ax0.plot(Tmiss_values, unavailabiltyData, label="Unavailability")
ax0.plot(Tmiss_values, unreliabilityFFData, label="Unreliability FF")
ax0.plot(Tmiss_values, unavailabiltyFFData, label="Unavailability FF")
ax0.legend()

ax1.set_title("Error Estimation")
ax1.plot(Tmiss_values, unreliabilityDataV, label="Unreliability")
ax1.plot(Tmiss_values, unavailabiltyDataV, label="Unavailability")
ax1.plot(Tmiss_values, unreliabilityFFDataV, label="Unreliability FF")
ax1.plot(Tmiss_values, unavailabiltyFFDataV, label="Unavailability FF")
ax1.legend()

plt.plot(Tmiss_values, unreliabilityFFData, label="Unavailability", color='red')
plt.title("Evolution of Unreliability and Unavailability with Tmiss")
plt.xlabel("Tmiss")
plt.ylabel("Probability")
plt.legend()
plt.grid()
plt.show()

