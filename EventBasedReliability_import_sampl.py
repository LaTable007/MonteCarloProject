import numpy as np
import matplotlib.pyplot as plt

# Seed for reproducibility
np.random.seed(1)

# Parameters
Lambda_1 = 0.0001
Lambda = 0.0001
Mu = 0.0001
Mu_1 = 0.0001
Tmiss_values = np.linspace(0.1, 10000, 50)
NumberSim = 10000

Lambda_Primme = 0.001
Mu_Primme = 0.0001
Lambda1_Primme = 0.001
Mu1_Primme = 0.0001

# Transition matrix and states
A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]

A_importance = [[-Lambda_1 * 2, 0, 0, Lambda_1 * 2, 0, 0],
                [Mu, -Mu - Lambda * 2, 0, 0, Lambda_1 * 2, 0],
                [0, 2 * Mu, -2 * Mu - Lambda_1 * 2, 0, 0, Lambda_1 * 2],
                [Mu_1, 0, 0, -Mu_1 - Lambda * 2, Lambda * 2, 0],
                [0, 0, 0, Mu, -Mu - Lambda * 2, Lambda * 2],
                [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]

#A_importance = [[-Lambda1_Primme, 0, 0, Lambda1_Primme, 0, 0], [Mu_Primme, -Mu_Primme - Lambda_Primme, 0, 0, Lambda1_Primme, 0],
#     [0, 2 * Mu_Primme, -2 * Mu_Primme - Lambda1_Primme, 0, 0, Lambda1_Primme], [Mu1_Primme, 0, 0, -Mu1_Primme - Lambda_Primme, Lambda_Primme, 0],
#     [0, 0, 0, Mu_Primme, -Mu_Primme - Lambda_Primme, Lambda_Primme], [0, 0, Mu1_Primme, 0, 2 * Mu_Primme, -Mu1_Primme - 2 * Mu_Primme]]

def NewStateSample(StateInd):
    times = []
    indices = []
    for i in range(len(A)):
        if i == StateInd or A[StateInd][i] == 0:
            continue
        etha = np.random.uniform(0, 1)
        v = -np.log(etha) / np.abs(A[StateInd][i])
        times.append(v)
        indices.append(i)
    if not times:  # Handle edge case where no transitions are possible
        return StateInd, np.inf
    mint = min(times)
    ind = times.index(mint)
    return indices[ind], mint

def NewStateSampleImportance(StateInd, matrix):
    """Sample new state and time using the modified importance sampling matrix."""
    times = []
    indices = []
    for i in range(len(matrix)):
        if i == StateInd or matrix[StateInd][i] == 0:
            continue
        etha = np.random.uniform(0, 1)
        v = -np.log(etha) / np.abs(matrix[StateInd][i])
        times.append(v)
        indices.append(i)
    if not times:  # Handle edge case where no transitions are possible
        return StateInd, np.inf
    mint = min(times)
    ind = times.index(mint)
    return indices[ind], mint

def Unreliability(numberSim, Tmiss):
    unreliable_states = []
    unavailable_states = []

    for i in range(numberSim):
        time = 0
        stateInd = 0
        Reliable = True
        unreliable = False
        unavailable = False

        while time <= Tmiss:
            sInd, t = NewStateSample(stateInd)
            time += t
            if time >= Tmiss:
                break
            stateInd = sInd
            if stateInd == 5 and Reliable:
                unreliable = True
                Reliable = False

        if stateInd == 5:
            unavailable = True

        unreliable_states.append(unreliable)
        unavailable_states.append(unavailable)

    # Calculate probabilities
    unreliability = np.mean(unreliable_states)
    unavailability = np.mean(unavailable_states)

    # Calculate variances
    unreliability_var = np.var(unreliable_states, ddof=1)
    unavailability_var = np.var(unavailable_states, ddof=1)

    return (
        unreliability,
        unavailability,
        np.sqrt(unreliability_var / numberSim),  # Standard error for unreliability
        np.sqrt(unavailability_var / numberSim)  # Standard error for unavailability
    )


def UnreliabilityBias(numberSim, Tmiss, A, A_Prime):
    """Simulate unreliability and unavailability with bias correction using weights."""
    numberUnreliableStates = 0
    numberUnavailableStates = 0
    UnreliableWeights = []
    UnavailableWeights = []

    for i in range(numberSim):
        time = 0
        stateInd = 0
        Reliable = True
        weight = 1

        while time <= Tmiss:
            # Sample le temps depuis la matrice A initiale
            sInd, t = NewStateSampleImportance(stateInd, A)
            time += t

            if time >= Tmiss:
                break

            # Calcul correction poids
            PreviousStateInd = stateInd
            stateInd = NewStateSampleImportance(stateInd, A_Prime)[0]
            weight *= (A[PreviousStateInd][stateInd] / A[PreviousStateInd][PreviousStateInd]) / (
                A_Prime[PreviousStateInd][stateInd] / A_Prime[PreviousStateInd][PreviousStateInd])

            if stateInd == 5 and Reliable:
                numberUnreliableStates += weight
                UnreliableWeights.append(weight)
                Reliable = False

        if stateInd == 5:
            numberUnavailableStates += weight
            UnavailableWeights.append(weight)

    return (
        numberUnreliableStates / numberSim,
        numberUnavailableStates / numberSim,
        np.std(UnreliableWeights) / np.sqrt(numberSim),  # Erreur standard unreliability
        np.std(UnavailableWeights) / np.sqrt(numberSim)
    )



unreliability_values = []
unavailability_values = []
unreliability_errors = []
unavailability_errors = []

unreliability_values_importance = []
unavailability_values_importance = []
unreliability_errors_importance = []
unavailability_errors_importance = []

for Tmiss in Tmiss_values:
    u_reliable, u_available, u_reliable_err, u_available_err = Unreliability(NumberSim, Tmiss)
    unreliability_values.append(u_reliable)
    unavailability_values.append(u_available)
    unreliability_errors.append(u_reliable_err)
    unavailability_errors.append(u_available_err)

    u_reliable, u_available, u_reliable_err, u_available_err = UnreliabilityBias(
        NumberSim, Tmiss, A, A_importance
    )
    unreliability_values_importance.append(u_reliable)
    unavailability_values_importance.append(u_available)
    unreliability_errors_importance.append(u_reliable_err)
    unavailability_errors_importance.append(u_available_err)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot unreliability et unavailability
axes[0].plot(Tmiss_values, unreliability_values, label="Unreliability", color='blue')
axes[0].plot(Tmiss_values, unavailability_values, label="Unavailability", color='red')
axes[0].plot(Tmiss_values, unreliability_values_importance, label="Unreliability (importance sampling)", color='purple')
axes[0].plot(Tmiss_values, unavailability_values_importance, label="Unavailability (importance sampling)", color='orange')
axes[0].set_title("Unreliability and Unavailability vs Tmiss")
axes[0].set_xlabel("Tmiss")
axes[0].set_ylabel("Probability")
axes[0].legend()
axes[0].grid()

# Plot erreurs standard
axes[1].plot(Tmiss_values, unreliability_errors, label="Unreliability ", color='blue', linestyle='--')
axes[1].plot(Tmiss_values, unavailability_errors, label="Unavailability", color='red', linestyle='--')
axes[1].plot(Tmiss_values, unreliability_errors_importance, label="Unreliability (importance sampling)", color='purple', linestyle='--')
axes[1].plot(Tmiss_values, unavailability_errors_importance, label="Unavailability (importance sampling)", color='orange', linestyle='--')
axes[1].set_title("Standard Error vs Tmiss")
axes[1].set_xlabel("Tmiss")
axes[1].set_ylabel("Standard Error")
axes[1].legend()
axes[1].grid()

plt.tight_layout()
plt.show()
