# On fait d'abord une partie unreliability ce sera plus simple dans un premier temp
# en system based-approach
import numpy as np
import matplotlib.pyplot as plt

#seed = 1
#np.random.seed(seed)

Lambda_1 = 0.00001
Lambda = 0.00001
Mu = 0.00001
Mu_1 = 0.00001


NumberSim = 10000

# 1 = operating, 0 = failed, 2 = stand-by
possible_states = [[1, 2, 2], [0, 1, 2], [0, 0, 1], [0, 0, 0], [1, 2, 0], [1, 0, 0]]
# on garde l'ordre dans choisi dans possible states pour donner un numero à chauqe état pour pouvoir les identifier dans le code
A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]
A_failure = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [0, - Lambda, 0, 0, Lambda_1, 0], 
            [0, 0, -Lambda_1, 0, 0, Lambda_1], [0, 0, 0, -Lambda, Lambda, 0],
            [0, 0, 0, 0, -Lambda, Lambda], [0, 0, 0, 0, 0, 0]]
failed_state = [0, 0, 0]
#NumberSim = 1000



def SejournTimeSampleForced(StateInd, A):
    etha = np.random.uniform(0, 1)
    sampled_time = -np.log(etha) / np.abs(A[StateInd][StateInd])
    return sampled_time

def NewStateSampleForced(StateInd, A, force_failure=False):
    if force_failure == False:
        etha = np.random.uniform(0, 1)
        P0 = 0
        P1 = 0  
        state = 0
        prob = 1
        for i in range(len(A)):
            if i == StateInd : continue
            P1 += A[StateInd][i] / np.abs(A[StateInd][StateInd])
            if P0 <= etha < P1:
                state = i
                break
            P0 += A[StateInd][i] / np.abs(A[StateInd][StateInd])
        return state, prob
    else:
        original_prob = abs(A[StateInd][StateInd])
        state = StateInd
        if StateInd == 0:
            state = 3
        elif StateInd == 1:
            state = 4
        elif StateInd == 2:
            state = 5
        elif StateInd == 3:
            state = 4
        elif StateInd == 4:
            state = 5
        elif StateInd == 5:
            state = 5
        return state, original_prob

        

def UnreliabilityForced(numberSim, Tmiss, A, t_bias):
    numberUnreliableStates_list = []
    numberUnavailableStates_list = []
    weight_list_r = []
    weight_list_u = []

    for i in range(numberSim):
        time = 0
        time2 = 0
        stateInd = 0
        Reliable = True
        weight = 1

        while time <= Tmiss:
            time_sampled = SejournTimeSampleForced(stateInd, A)
            time += time_sampled
            time2 += time_sampled
            if time >= Tmiss: break

            if time2 <= t_bias:   
                stateInd, weight = NewStateSampleForced(stateInd, A)
                weight *= weight

            if time2 > t_bias:                
                stateInd, weight = NewStateSampleForced(stateInd, A, force_failure=True)
                weight *= weight
                """
                if stateInd == 5:
                    print("Forcing failure and 5", weight)
                if stateInd == 5 and Reliable:
                    print("Forcing failure, 5 and Reliable", weight)
                """
                time2 = 0

            if stateInd == 5 and Reliable:
                numberUnreliableStates_list.append(weight)
                weight_list_r.append(weight)
                print(weight)
                Reliable = False

        if stateInd == 5:
            numberUnavailableStates_list.append(weight)
            weight_list_u.append(weight)

    return np.array(numberUnreliableStates_list), np.array(numberUnavailableStates_list), np.array(weight_list_r), np.array(weight_list_u)

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

    return SE




# Valeurs de t_bias à tester
T_bias_values = [1000, 10000]
Tmiss_values = np.linspace(0.1, 10000, 50)

""""

# Stockage des résultats pour chaque t_bias
results_unreliability = {}
results_unavailability = {}

for t_bias in T_bias_values:
    unreliability_values = []
    unavailability_values = []
    
    for Tmiss in Tmiss_values:
        u_reliable, u_available, _ = UnreliabilityForced(NumberSim, Tmiss, A, t_bias)
        unreliability_values.append(u_reliable.sum() / NumberSim)
        unavailability_values.append(u_available.sum() / NumberSim)
    
    results_unreliability[t_bias] = unreliability_values
    results_unavailability[t_bias] = unavailability_values

# Affichage des courbes
plt.figure(figsize=(12, 8))

# Courbes d'unreliability
for t_bias, values in results_unreliability.items():
    plt.plot(Tmiss_values, values, label=f"Unreliability (t_bias={t_bias})")

plt.title("Unreliability with Different t_bias")
plt.xlabel("Tmiss")
plt.ylabel("Probability")
plt.legend()
plt.grid()
plt.show()

# Courbes d'unavailability
plt.figure(figsize=(12, 8))

for t_bias, values in results_unavailability.items():
    plt.plot(Tmiss_values, values, label=f"Unavailability (t_bias={t_bias})")

plt.title("Unavailability with Different t_bias")
plt.xlabel("Tmiss")
plt.ylabel("Probability")
plt.legend()
plt.grid()
plt.show()
"""

# Stockage des résultats
results_unreliability = []
results_unavailability = []


for T_bias in T_bias_values:
    SE_unreliability = []
    SE_unavailability = []
    for Tmiss in Tmiss_values:
        # Simuler la méthode avec les paramètres actuels
        unreliable, unavailable, weights_r, weights_u = UnreliabilityForced(NumberSim, Tmiss, A, T_bias)
        
        # Calculer l'erreur standard pour unreliability
        SE_unreliability.append(compute_accuracy_metrics(unreliable, weights_r))

        # Calculer l'erreur standard pour unavailability
        SE_unavailability.append(compute_accuracy_metrics(unavailable, weights_u))

    results_unreliability.append(SE_unreliability)
    results_unavailability.append(SE_unavailability)

# Tracer les graphiques
plt.figure(figsize=(14, 6))

# Graphique pour l'unreliability
plt.subplot(1, 2, 1)
for idx, T_bias in enumerate(T_bias_values):
    plt.plot(Tmiss_values, results_unreliability[idx], label=f'T_bias = {T_bias}')
plt.title('Précision de l unreliability en fonction de Tmiss')
plt.xlabel('Tmiss')
plt.ylabel('Erreur standard (SE)')
plt.legend()
plt.grid()

# Graphique pour l'unavailability
plt.subplot(1, 2, 2)
for idx, T_bias in enumerate(T_bias_values):
    plt.plot(Tmiss_values, results_unavailability[idx], label=f'T_bias = {T_bias}')
plt.title('Précision de l unavailability en fonction de Tmiss')
plt.xlabel('Tmiss')
plt.ylabel('Erreur standard (SE)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()


