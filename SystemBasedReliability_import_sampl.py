import numpy as np
import matplotlib.pyplot as plt
import time

seed = 1
np.random.seed(seed)

Lambda_1 = 0.0001
Lambda = 0.0001
Mu = 0.0001
Mu_1 = 0.0001
Tmiss = 1

possible_states = [[1, 2, 2], [0, 1, 2], [0, 0, 1], [0, 0, 0], [1, 2, 0], [1, 0, 0]]
A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]

NumberSim = 100000


def SejournTimeSample(StateInd):
    etha = np.random.uniform(0, 1)
    return -np.log(etha) / np.abs(A[StateInd][StateInd])


def NewStateSampleWithBias(StateInd, bias_factors):
    etha = np.random.uniform(0, 1)
    P0 = 0
    P1 = 0
    state = 0
    for i in range(len(A)):
        if i == StateInd:
            continue
        # Apply the bias factor to the transition probability
        adjusted_rate = A[StateInd][i] * bias_factors[i]
        P1 += adjusted_rate / np.abs(A[StateInd][StateInd])
        if P0 <= etha < P1:
            state = i
            break
        P0 += adjusted_rate / np.abs(A[StateInd][StateInd])
    return state

def NewStateSample(StateInd):
    etha = np.random.uniform(0, 1)
    P0 = 0
    P1 = 0
    state = 0
    for i in range(len(A)):
        if i == StateInd: continue
        P1 += A[StateInd][i] / np.abs(A[StateInd][StateInd])
        if P0 <= etha < P1:
            state = i
            break
        P0 += A[StateInd][i] / np.abs(A[StateInd][StateInd])
    return state



def UnreliabilityWithImportanceSampling(numberSim, Tmiss):
    bias_factors = [1.0, 1.1666666666666665, 1.5, 1.0, 1.3333333333333333, 1.5] # Bias higher for failure states
    unreliability_list = []
    unavailability_list = []
    weights = []

    for _ in range(numberSim):
        time = 0
        stateInd = 0
        reliable = True
        weight = 1.0

        while time <= Tmiss:
            time += SejournTimeSample(stateInd)
            if time >= Tmiss:
                break

            new_state = NewStateSampleWithBias(stateInd, bias_factors)
            # Calculate weight correction factor
            weight *= A[stateInd][new_state] / (A[stateInd][new_state] * bias_factors[new_state])
            stateInd = new_state

            if stateInd == 5 and reliable:
                unreliability_list.append(1 * weight)
                reliable = False

        if stateInd == 5:
            unavailability_list.append(1 * weight)
        else:
            unavailability_list.append(0)
        if reliable:
            unreliability_list.append(0)

        weights.append(weight)

    return np.array(unreliability_list), np.array(unavailability_list), np.array(weights)

def Unreliability(numberSim, Tmiss):
    unreliability_list = []
    unavailability_list = []

    # on va faire un nombre n fois l'evolution du systeme
    for _ in range(numberSim):
        # etat initial du systeme : la unit 1 operationel (1), les 2 autres en cold stand-by (2)
        time = 0
        stateInd = 0
        reliable = True

        while time <= Tmiss:
            # sample de la durée pendant laquel il n'y a pas d'evolution du système
            time += SejournTimeSample(stateInd)
            if time >= Tmiss: break
            stateInd = NewStateSample(stateInd)
            #print(stateInd)
            if stateInd == 5 and reliable:
                unreliability_list.append(1)
                Reliable = False

        if stateInd == 5:
            unavailability_list.append(1)
        else:
            unavailability_list.append(0)
        if reliable:
            unreliability_list.append(0)

    return np.array(unreliability_list), np.array(unavailability_list)


def compute_accuracy_metrics(values, weights):
    """
    Compute accuracy metrics for the simulation results.

    Parameters:
    values (np.array): Simulation results (e.g., unreliability/unavailability).
    weights (np.array): Corresponding weights for the results.

    Returns:
    dict: Accuracy metrics including SE, CI Width, and ESS.
    """
    weighted_mean = np.sum(values * weights) / np.sum(weights)
    weighted_variance = np.sum(weights * (values - weighted_mean) ** 2) / np.sum(weights)
    SE = np.sqrt(weighted_variance / len(values))
    CI_width = 2 * 1.96 * SE  # 95% confidence interval
    ESS = (np.sum(weights) ** 2) / np.sum(weights ** 2)

    return {
        "Weighted Mean": weighted_mean,
        "Variance": weighted_variance,
        "Standard Error": SE,
        "CI Width": CI_width,
        "Effective Sample Size": ESS
    }


# Measure execution time
start_time = time.time()

# Vectors for Tmiss and results
Tmiss_values = np.linspace(0.1, 10000, 50)
unreliability_mean = []
unreliability_CI = []
unavailability_mean = []
unavailability_CI = []
metrics_list = []  # Store accuracy metrics for each Tmiss

unreliability_v_mean = []
unreliability_v_CI = []
unavailability_v_mean = []
unavailability_v_CI = []

for Tmiss in Tmiss_values:
    u_reliable, u_available, weights = UnreliabilityWithImportanceSampling(NumberSim, Tmiss)

    # Weighted mean and variance for unreliability
    mean_reliable = np.sum(u_reliable) / np.sum(weights)
    variance_reliable = np.var(u_reliable / weights)
    SE_reliable = np.sqrt(variance_reliable / NumberSim)
    CI_reliable = 1.96 * SE_reliable

    # Weighted mean and variance for unavailability
    mean_available = np.sum(u_available) / np.sum(weights)
    variance_available = np.var(u_available / weights)
    SE_available = np.sqrt(variance_available / NumberSim)
    CI_available = 1.96 * SE_available

    unreliability_mean.append(mean_reliable)
    unreliability_CI.append(CI_reliable)
    unavailability_mean.append(mean_available)
    unavailability_CI.append(CI_available)

    u_reliable_v, u_available_v = Unreliability(NumberSim, Tmiss)

    # Calcule la moyenne et l'interval de confiance pour l'unreliability
    mean_reliable_v = np.mean(u_reliable_v)
    variance_reliable_v = np.var(u_reliable_v)
    SE_reliable_v = np.sqrt(variance_reliable_v / NumberSim)  # Erreur standard
    CI_reliable_v = 1.96 * SE_reliable_v  # Interval de confiance de 95%

    # Calcule la moyenne et l'interval de confiance pour l'unavailibility
    mean_available_v = np.mean(u_available_v)
    variance_available_v = np.var(u_available_v)
    SE_available_v = np.sqrt(variance_available_v / NumberSim)
    CI_available_v = 1.96 * SE_available_v

    unreliability_v_mean.append(mean_reliable_v)
    unreliability_v_CI.append(CI_reliable_v)
    unavailability_v_mean.append(mean_available_v)
    unavailability_v_CI.append(CI_available_v)

    # Compute accuracy metrics
    metrics = compute_accuracy_metrics(u_reliable, weights)
    metrics_list.append(metrics)

end_time = time.time()

# Execution time
elapsed_time = end_time - start_time
print(f"Total execution time with importance sampling: {elapsed_time:} seconds")

# Extract metrics for plotting
SEs = [metrics["Standard Error"] for metrics in metrics_list]
CI_widths = [metrics["CI Width"] for metrics in metrics_list]
ESS_values = [metrics["Effective Sample Size"] for metrics in metrics_list]

SEs = [metrics["Standard Error"] for metrics in metrics_list]
CI_widths = [metrics["CI Width"] for metrics in metrics_list]
ESS_values = [metrics["Effective Sample Size"] for metrics in metrics_list]

# Define the figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))  # 2 rows, 2 columns

# Plot Standard Error vs Tmiss
axes[0, 0].plot(Tmiss_values, SEs, label="Standard Error (SE)", color='green')
axes[0, 0].set_title("Standard Error vs Tmiss")
axes[0, 0].set_xlabel("Tmiss")
axes[0, 0].set_ylabel("Standard Error")
axes[0, 0].grid()
axes[0, 0].legend()

# Plot Confidence Interval Width vs Tmiss
axes[0, 1].plot(Tmiss_values, CI_widths, label="Confidence Interval Width", color='purple')
axes[0, 1].set_title("Confidence Interval Width vs Tmiss")
axes[0, 1].set_xlabel("Tmiss")
axes[0, 1].set_ylabel("CI Width")
axes[0, 1].grid()
axes[0, 1].legend()

# Plot Effective Sample Size vs Tmiss
axes[1, 0].plot(Tmiss_values, ESS_values, label="Effective Sample Size (ESS)", color='orange')
axes[1, 0].set_title("Effective Sample Size vs Tmiss")
axes[1, 0].set_xlabel("Tmiss")
axes[1, 0].set_ylabel("ESS")
axes[1, 0].grid()
axes[1, 0].legend()

# Plot Unreliability and Unavailability with CI vs Tmiss
axes[1, 1].plot(Tmiss_values, unreliability_mean, label="Unreliability (Importance Sampling)", color='blue')
axes[1, 1].fill_between(Tmiss_values, np.array(unreliability_mean) - np.array(unreliability_CI),
                         np.array(unreliability_mean) + np.array(unreliability_CI), color='blue', alpha=0.3)
axes[1, 1].plot(Tmiss_values, unavailability_mean, label="Unavailability (Importance Sampling)", color='red')
axes[1, 1].fill_between(Tmiss_values, np.array(unavailability_mean) - np.array(unavailability_CI),
                         np.array(unavailability_mean) + np.array(unavailability_CI), color='red', alpha=0.3)
axes[1, 1].set_title("Evolution of Unreliability and Unavailability with Tmiss")
axes[1, 1].set_xlabel("Tmiss")
axes[1, 1].set_ylabel("Probability")
axes[1, 1].grid()
axes[1, 1].legend()


axes[1, 1].plot(Tmiss_values, unreliability_v_mean, label="Unreliability (Importance Sampling)", color='purple')
axes[1, 1].fill_between(Tmiss_values, np.array(unreliability_v_mean) - np.array(unreliability_v_CI),
                         np.array(unreliability_v_mean) + np.array(unreliability_v_CI), color='purple', alpha=0.3)
axes[1, 1].plot(Tmiss_values, unavailability_v_mean, label="Unavailability (Importance Sampling)", color='orange')
axes[1, 1].fill_between(Tmiss_values, np.array(unavailability_v_mean) - np.array(unavailability_v_CI),
                         np.array(unavailability_v_mean) + np.array(unavailability_v_CI), color='orange', alpha=0.3)
axes[1, 1].set_title("Evolution of Unreliability and Unavailability with Tmiss")
axes[1, 1].set_xlabel("Tmiss")
axes[1, 1].set_ylabel("Probability")
axes[1, 1].grid()
axes[1, 1].legend()


# Adjust layout for better spacing
plt.tight_layout()
plt.show()

