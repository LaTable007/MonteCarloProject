import numpy as np
import matplotlib.pyplot as plt
import time

#seed = 1
#np.random.seed(seed)

Lambda_1 = 0.0001
Lambda = 0.0001
Mu = 0.0001
Mu_1 = 0.0001
Tmiss = 1

# 1 = operating, 0 = failed, 2 = stand-by
possible_states = [[1, 2, 2], [0, 1, 2], [0, 0, 1], [0, 0, 0], [1, 2, 0], [1, 0, 0]]
# on garde l'ordre dans choisi dans possible states pour donner un numero à chauqe état pour pouvoir les identifier dans le code
A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]

NumberSim = 100000


def SejournTimeSample(StateInd):
    etha = np.random.uniform(0, 1)
    return -np.log(etha) / np.abs(A[StateInd][StateInd])


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

def NewStateSampleWithBias(StateInd, bias_factors):
    etha = np.random.uniform(0, 1)
    P0 = 0
    P1 = 0
    state = 0
    for i in range(len(A)):
        if i == StateInd:
            continue
        # On multiplie par le bias factor
        adjusted_rate = A[StateInd][i] * bias_factors[i]
        P1 += adjusted_rate / np.abs(A[StateInd][StateInd])
        if P0 <= etha < P1:
            state = i
            break
        P0 += adjusted_rate / np.abs(A[StateInd][StateInd])
    #print(P1)
    return state

def UnreliabilityWithImportanceSampling(numberSim, Tmiss):
    #bias_factors = [1.0, 1.1666666666666665, 1.5, 1.0, 1.3333333333333333, 1.5] # Biais plus important pour états failed
    bias_factors  = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
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
            # Calcule le facteur de correction pour le poids
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


def compute_accuracy_metrics(values, weights=None):
    if weights is None:
        # Cas sans importance sampling
        weights = np.ones_like(values)

    # Moyenne pondérée
    weighted_mean = np.sum(values * weights) / np.sum(weights)

    # Variance pondérée
    weighted_variance = np.sum(weights * (values - weighted_mean) ** 2) / np.sum(weights)

    # Erreur standard
    SE = np.sqrt(weighted_variance / len(values))

    # Interval de confiance (95%)
    CI_width = 2 * 1.96 * SE

    # Effective sample size (ESS)
    ESS = (np.sum(weights) ** 2) / np.sum(weights ** 2)

    return {
        "Weighted Mean": weighted_mean,
        "Variance": weighted_variance,
        "Standard Error": SE,
        "CI Width": CI_width,
        "Effective Sample Size": ESS
    }

#Mesure du temps d'execution
start_time = time.time()

# Vecteurs pour les différents Tmiss et résultats
Tmiss_values = np.linspace(0.1, 10000, 50)
unreliability_mean = []
unreliability_CI = []
unavailability_mean = []
unavailability_CI = []
metrics_list = []  # Mesures de précision

unreliability_v_mean = []
unreliability_v_CI = []
unavailability_v_mean = []
unavailability_v_CI = []
metrics_list_v = []  # Mesures de précision

for Tmiss in Tmiss_values:
    u_reliable, u_available, weights = UnreliabilityWithImportanceSampling(NumberSim, Tmiss)

    # Calcule la moyenne et l'interval de confiance pour l'unreliability
    mean_reliable = np.sum(u_reliable) / np.sum(weights)
    variance_reliable = np.var(u_reliable / weights)
    SE_reliable = np.sqrt(variance_reliable / NumberSim)
    CI_reliable = 1.96 * SE_reliable

    # Calcule la moyenne et l'interval de confiance pour l'unavailibility
    mean_available = np.sum(u_available) / np.sum(weights)
    variance_available = np.var(u_available / weights)
    SE_available = np.sqrt(variance_available / NumberSim)
    CI_available = 1.96 * SE_available

    unreliability_mean.append(mean_reliable)
    unreliability_CI.append(CI_reliable)
    unavailability_mean.append(mean_available)
    unavailability_CI.append(CI_available)

    # Calcule des mesures de précision (avec "importance sampling")
    metrics = compute_accuracy_metrics(u_reliable, weights)
    metrics_list.append(metrics)

    #Cas standard (sans "importance sampling")

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

    # Calcule des mesures de précision cas standard
    metrics_v = compute_accuracy_metrics(u_reliable_v)
    metrics_list_v.append(metrics_v)

end_time = time.time()

#Temps d'éxecution
elapsed_time = end_time - start_time
print(f"Total execution time with importance sampling: {elapsed_time:} seconds")

SEs = [metrics["Standard Error"] for metrics in metrics_list]
CI_widths = [metrics["CI Width"] for metrics in metrics_list]
ESS_values = [metrics["Effective Sample Size"] for metrics in metrics_list]

SEs_v = [metrics["Standard Error"] for metrics in metrics_list_v]
CI_widths_v = [metrics["CI Width"] for metrics in metrics_list_v]
ESS_values_v = [metrics["Effective Sample Size"] for metrics in metrics_list_v]


fig, axes = plt.subplots(2, 2, figsize=(16, 12))  # 2 rows, 2 columns

# Plot de l'erreur standard vs Tmiss
axes[0, 0].plot(Tmiss_values, SEs, label="Standard Error (SE) (Importance Sampling)", color='blue')
axes[0, 0].plot(Tmiss_values, SEs_v, label="Standard Error (SE)", color='purple')
axes[0, 0].set_title("Standard Error vs Tmiss")
axes[0, 0].set_xlabel("Tmiss")
axes[0, 0].set_ylabel("Standard Error")
axes[0, 0].grid()
axes[0, 0].legend()

# Plot de l'interval de confiance vs Tmiss
axes[0, 1].plot(Tmiss_values, CI_widths, label="Confidence Interval Width (Importance Sampling)", color='blue')
axes[0, 1].plot(Tmiss_values, CI_widths_v, label="Confidence Interval Width", color='purple')
axes[0, 1].set_title("Confidence Interval Width vs Tmiss")
axes[0, 1].set_xlabel("Tmiss")
axes[0, 1].set_ylabel("CI Width")
axes[0, 1].grid()
axes[0, 1].legend()

# Plot de l'EES vs Tmiss
axes[1, 0].plot(Tmiss_values, ESS_values, label="Effective Sample Size (ESS) (Importance Sampling)", color='blue')
axes[1, 0].plot(Tmiss_values, ESS_values_v, label="Effective Sample Size (ESS)", color='purple')
axes[1, 0].set_title("Effective Sample Size vs Tmiss")
axes[1, 0].set_xlabel("Tmiss")
axes[1, 0].set_ylabel("ESS")
axes[1, 0].grid()
axes[1, 0].legend()


# Plot de l'Unreliability et Unavailability vs Tmiss
axes[1, 1].plot(Tmiss_values, unreliability_v_mean, label="Unreliability", color='blue')
axes[1, 1].fill_between(Tmiss_values, np.array(unreliability_v_mean) - np.array(unreliability_v_CI),
                         np.array(unreliability_v_mean) + np.array(unreliability_v_CI), color='blue', alpha=0.3)
axes[1, 1].plot(Tmiss_values, unavailability_v_mean, label="Unavailability", color='red')
axes[1, 1].fill_between(Tmiss_values, np.array(unavailability_v_mean) - np.array(unavailability_v_CI),
                         np.array(unavailability_v_mean) + np.array(unavailability_v_CI), color='red', alpha=0.3)


axes[1, 1].set_title("Evolution of Unreliability and Unavailability with Tmiss")
axes[1, 1].set_xlabel("Tmiss")
axes[1, 1].set_ylabel("Probability")
axes[1, 1].grid()
axes[1, 1].legend()

plt.tight_layout()
plt.show()

