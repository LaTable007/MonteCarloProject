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

def Unreliability_with_details(numberSim, Tmiss):
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


def Unreliability_with_importance(numberSim, Tmiss, original_matrix, importance_matrix):
    unreliable_states = []
    unavailable_states = []
    weights = []

    for i in range(numberSim):
        time = 0
        stateInd = 0
        Reliable = True
        unreliable = False
        unavailable = False
        weight = 1.0

        while time <= Tmiss:
            # sample a partir de la matrice modifiée
            sInd, t = NewStateSampleImportance(stateInd, importance_matrix)
            time += t
            if time >= Tmiss:
                break

            # Calcule des corrections pour le poids
            if importance_matrix[stateInd][sInd] != 0:
                weight *= original_matrix[stateInd][sInd] / importance_matrix[stateInd][sInd]

            stateInd = sInd
            if stateInd == 5 and Reliable:
                unreliable = True
                Reliable = False

        if stateInd == 5:
            unavailable = True

        unreliable_states.append(unreliable * weight)
        unavailable_states.append(unavailable * weight)
        weights.append(weight)

    # On divise par les poids pour corriger le biais
    total_weight = np.sum(weights)
    unreliability = np.sum(unreliable_states) / total_weight
    unavailability = np.sum(unavailable_states) / total_weight

    # Calculate des variances pondérées pour l'erreur standard
    unreliability_var = np.sum(weights * (np.array(unreliable_states) / weights - unreliability) ** 2) / total_weight
    unavailability_var = np.sum(weights * (np.array(unavailable_states) / weights - unavailability) ** 2) / total_weight

    return (
        unreliability,
        unavailability,
        np.sqrt(unreliability_var / numberSim),  # Erreur standard unreliability
        np.sqrt(unavailability_var / numberSim)
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
    u_reliable, u_available, u_reliable_err, u_available_err = Unreliability_with_details(NumberSim, Tmiss)
    unreliability_values.append(u_reliable)
    unavailability_values.append(u_available)
    unreliability_errors.append(u_reliable_err)
    unavailability_errors.append(u_available_err)

    u_reliable, u_available, u_reliable_err, u_available_err = Unreliability_with_importance(
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
axes[0].plot(Tmiss_values, unreliability_values_importance, label="Unreliability", color='purple')
axes[0].plot(Tmiss_values, unavailability_values_importance, label="Unavailability", color='orange')
axes[0].set_title("Unreliability and Unavailability vs Tmiss")
axes[0].set_xlabel("Tmiss")
axes[0].set_ylabel("Probability")
axes[0].legend()
axes[0].grid()

# Plot erreurs standard
axes[1].plot(Tmiss_values, unreliability_errors, label="Unreliability (importance sampling)", color='blue', linestyle='--')
axes[1].plot(Tmiss_values, unavailability_errors, label="Unavailability (importance sampling)", color='red', linestyle='--')
axes[1].plot(Tmiss_values, unreliability_errors_importance, label="Unreliability", color='purple', linestyle='--')
axes[1].plot(Tmiss_values, unavailability_errors_importance, label="Unavailability", color='orange', linestyle='--')
axes[1].set_title("Standard Error vs Tmiss")
axes[1].set_xlabel("Tmiss")
axes[1].set_ylabel("Standard Error")
axes[1].legend()
axes[1].grid()

plt.tight_layout()
plt.show()
