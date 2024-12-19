import numpy as np
import matplotlib.pyplot as plt
from CommonFunctionsReliability import Unreliability, UnreliabilityFFSystemBased, VarianceCalculation, ErrorEstimation

# Définition des paramètres
Lambda_1 = 0.0001
Lambda = 0.0001
Mu = 0.0001
Mu_1 = 0.0001
NumberSim = 1000

# Matrice des transitions et état défaillant
A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]


def NewStateSampleEventBasedBias(StateInd, T_bias):
    times = []
    indices = []
    for i in range(len(A)):
        if i == StateInd or A[StateInd][i] == 0 : continue
        etha = np.random.uniform(0, 1)
        time = -np.log(1 - etha*(1-np.exp(-np.abs(A[StateInd][i])*T_bias)))/np.abs(A[StateInd][i])
        times.append(time)
        indices.append(i)
    mint = min(times)

    ind = times.index(mint)
    weight = CalculateWeight(StateInd, indices[ind], mint, T_bias)
    #print(weight)
    return indices[ind], times[ind], weight

def CalculateWeight(StateInd, NextStateInd, time, T_bias):
    #print("___________")
    weight_num = 1 - np.exp(-np.abs(A[StateInd][NextStateInd])*T_bias)
    #print(weight_num)
    #print(weight_num)
    weight_den = 1
    for i in range(len(A)):
        if i == StateInd or i == NextStateInd or A[StateInd][i] == 0: continue
        weight_num *= np.exp(-np.abs(A[StateInd][i])*time)
        weight_den *= 1 - (1 - np.exp(-np.abs(A[StateInd][i])*time))/(1 - np.exp(-np.abs(A[StateInd][i])*T_bias))
    #print("_____________")
    return weight_num/weight_den

def NewStateSampleEventBased(StateInd):
    times = []
    indices = []
    for i in range(len(A)):
        if i == StateInd or A[StateInd][i] == 0 : continue
        etha = np.random.uniform(0, 1)
        v = -np.log(etha)/np.abs(A[StateInd][i])
        times.append(v)
        indices.append(i)
    mint = min(times)

    ind = times.index(mint)
    return indices[ind], times[ind]




def UnreliabilityEventBasedBias(numberSim, Tmiss, T_bias):
    numberUnreliableStates = 0
    numberUnavailableStates = 0
    UnavailableWeights = []
    UnreliableWeights = []
    # on va faire un nombre n fois l'evolution du systeme
    for i in range(numberSim):
        # etat initial du systeme : la unit 1 operationel (1), les 2 autres en cold stand-by (2)
        time = 0
        stateInd = 0
        Reliable = True
        weights = 1

        while time <= Tmiss:
            # sample de la durée pendant laquel il n'y a pas d'evolution du système
            if Reliable:
                sInd, t, weight = NewStateSampleEventBasedBias(stateInd, T_bias)
                #print(weight)
            else:
                sInd, t = NewStateSampleEventBased(stateInd)
                weight = 1
            time += t
            weights *= weight
            if time >= Tmiss: break
            stateInd = sInd
            if stateInd == 5 and Reliable:
                numberUnreliableStates += weights
                UnreliableWeights.append(weight)
                Reliable = False

        if stateInd == 5:
            numberUnavailableStates += weights
            UnavailableWeights.append(weights)
    return numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights


def UnreliabilityEventBased(numberSim, Tmiss):
    numberUnreliableStates = 0
    numberUnavailableStates = 0
    # on va faire un nombre n fois l'evolution du systeme
    for i in range(numberSim):
        # etat initial du systeme : la unit 1 operationel (1), les 2 autres en cold stand-by (2)
        time = 0
        stateInd = 0
        Reliable = True

        while time <= Tmiss:
            # sample de la durée pendant laquel il n'y a pas d'evolution du système
            sInd, t = NewStateSampleEventBased(stateInd)
            time += t
            if time >= Tmiss: break
            stateInd = sInd
            if stateInd == 5 and Reliable:
                numberUnreliableStates += 1
                Reliable = False

        if stateInd == 5:
            numberUnavailableStates += 1
    return numberUnreliableStates, numberUnavailableStates

unreliabilityData = []
unavailabiltyData = []
unreliabilityFFData = []
unavailabiltyFFData = []
unreliabilityDataV = []
unavailabiltyDataV = []
unreliabilityFFDataV = []
unavailabiltyFFDataV = []
Tmiss = 0
numberSim = 10000

for j in range(100):
     Tmiss += 100
     print(Tmiss)
     numberUnreliableStates, numberUnavailableStates = Unreliability(numberSim, Tmiss, A)
     unreliabilityData.append(numberUnreliableStates/numberSim)
     unavailabiltyData.append(numberUnavailableStates/numberSim)
     unreliabilityDataV.append(VarianceCalculation(numberSim, numberUnreliableStates))
     unavailabiltyDataV.append(VarianceCalculation(numberSim, numberUnavailableStates))
     numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights = UnreliabilityEventBasedBias(numberSim, Tmiss, 1.4 *Tmiss)
     unreliabilityFFData.append(numberUnreliableStates / numberSim)
     unavailabiltyFFData.append(numberUnavailableStates / numberSim)
     unreliabilityFFDataV.append(ErrorEstimation(UnreliableWeights, numberSim,numberUnreliableStates))
     unavailabiltyFFDataV.append(ErrorEstimation(UnavailableWeights, numberSim,numberUnavailableStates))
Tmiss_values = [(i + 1)*100 for i in range(100)]
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

"""
numberSim = 10000
Tmiss = 10000
T_bias = 1.4*Tmiss
numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights = UnreliabilityFFSystemBased(numberSim, Tmiss, A)
print(numberUnreliableStates)
numberUnreliableStates, numberUnavailableStates = Unreliability(numberSim, Tmiss, A)
print(numberUnreliableStates)
numberUnreliableStates, numberUnavailableStates = UnreliabilityEventBasedBias(numberSim, Tmiss, T_bias)
print(numberUnreliableStates)


# Vecteurs pour les différents Tmiss et résultats
Tmiss_values = np.linspace(0.1, 10000, 50)


# Différentes valeurs de T_bias à analyser
T_bias_values = [10100, 11000, 20000]

# Stockage des résultats
results_unreliable_bias = {T_bias: [] for T_bias in T_bias_values}
results_unavailable_bias = {T_bias: [] for T_bias in T_bias_values}

results_unreliable = []
results_unavailable = []

# Calcul pour chaque T_bias
for T_bias in T_bias_values:
    for Tmiss in Tmiss_values:
        print(Tmiss)
        unreliable_bias, unavailable_bias = UnreliabilityEventBasedBias(NumberSim, Tmiss, T_bias)
        results_unreliable_bias[T_bias].append(unreliable_bias/NumberSim)
        results_unavailable_bias[T_bias].append(unavailable_bias/NumberSim)


for Tmiss in Tmiss_values:
    unreliable, unavailable = UnreliabilityEventBased(NumberSim, Tmiss)
    results_unreliable.append(unreliable/NumberSim)
    results_unavailable.append(unavailable/NumberSim)


# Tracer les résultats
plt.figure(figsize=(12, 6))

# Graphique pour les états non fiables
plt.subplot(1, 2, 1)
for T_bias in T_bias_values:
    plt.plot(Tmiss_values, results_unreliable_bias[T_bias], label=f"T_bias={T_bias}")
#plt.plot(Tmiss_values, results_unreliable, label="Without T_bias", linestyle="--")
plt.xlabel("Tmiss")
plt.ylabel("Unreliable States")
plt.title("Unreliable States vs Tmiss")
plt.legend()
plt.grid()

# Graphique pour les états indisponibles
plt.subplot(1, 2, 2)
for T_bias in T_bias_values:
    plt.plot(Tmiss_values, results_unavailable_bias[T_bias], label=f"T_bias={T_bias}")
#plt.plot(Tmiss_values, results_unavailable, label="Without T_bias", linestyle="--")
plt.xlabel("Tmiss")
plt.ylabel("Unavailable States")
plt.title("Unavailable States vs Tmiss")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
"""
