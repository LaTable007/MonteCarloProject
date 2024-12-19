# On fait d'abord une partie unreliability ce sera plus simple dans un premier temp
# en system based-approach
from CommonFunctionsReliability import *
import numpy as np
import matplotlib.pyplot as plt

#seed = 1
#np.random.seed(seed)

Lambda_1 = 0.001
Lambda = 0.001
Mu = 0.001
Mu_1 = 0.001

Lambda_Primme = 0.0001
Mu_Primme = 0.0001
Lambda1_Primme = 0.0001
Mu1_Primme = 0.0001
Tmiss = 10000
numberSim = 1000

# 1 = operating, 0 = failed, 2 = stand-by
possible_states = [[1, 2, 2], [0, 1, 2], [0, 0, 1], [0, 0, 0], [1, 2, 0], [1, 0, 0]]
# on garde l'ordre dans choisi dans possible states pour donner un numero à chauqe état pour pouvoir les identifier dans le code
A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]


numberUnreliableStates, numberUnavailableStates = Unreliability(numberSim, Tmiss, A)
print(numberUnreliableStates/numberSim, VarianceCalculation(numberSim, numberUnreliableStates))
numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights = UnreliabilityFFSystemBased(numberSim, Tmiss, A)
print(numberUnreliableStates/numberSim, ErrorEstimation(UnreliableWeights, numberSim, numberUnreliableStates))




# Création des plots
"""
plt.figure(figsize=(10, 6))
plt.plot(Tmiss_values, unreliability_values, label="Unreliability", color='blue')
plt.plot(Tmiss_values, unavailability_values, label="Unavailability", color='red')
plt.title("Evolution of Unreliability and Unavailability with Tmiss")
plt.xlabel("Tmiss")
plt.ylabel("Probability")
plt.legend()
plt.grid()
plt.show()
"""
