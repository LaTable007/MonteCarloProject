import numpy as np
import matplotlib.pyplot as plt


# Définition des paramètres
Lambda_1 = 0.0001
Lambda = 0.0001
Mu = 0.0001
Mu_1 = 0.0001
NumberSim = 10000

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
        time = -np.log(1 - etha*(1-np.exp(-A[StateInd][i]*T_bias)))/np.abs(A[StateInd][i])
        times.append(time)
        indices.append(i)
    mint = min(times)

    ind = times.index(mint)
    weight = CalculateWeight(ind, mint, T_bias)
    #print(weight)
    return indices[ind], times[ind], weight

def CalculateWeight(StateInd, time, T_bias):
    weight_num = 1
    weight_den = 1
    for i in range(len(A)):
        if A[StateInd][i] != 0:
            weight_num *= np.exp(-np.abs(A[StateInd][i])*T_bias)
        if i != StateInd and A[StateInd][i] != 0:
            weight_den *= 1 - (np.exp(-np.abs(A[StateInd][i])*T_bias)/np.exp(-np.abs(A[StateInd][i])*time))
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
                Reliable = False

        if stateInd == 5:
            numberUnavailableStates += weights
    return numberUnreliableStates, numberUnavailableStates


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

