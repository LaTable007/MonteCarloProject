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

# Vecteurs pour les résultats
Tmiss_values = np.linspace(0.1, 10000, 50)
Tbias_values = [100, 1000, 10000]
colors = ['tab:blue', 'tab:green', 'tab:orange']

# Fonction pour obtenir l'état suivant
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
    mint = min(times)
    ind = times.index(mint)
    return indices[ind], times[ind]

# Fonction pour calculer l'Unreliability avec correction du biais
def Unreliability(numberSim, Tmiss, Tbias, Lambda_bias):
    weighted_unreliable = []
    weighted_unavailable = []
    weights = []

    
    for _ in range(numberSim):
        time = 0
        stateInd = 0
        Reliable = True
        weight = 1

        while time <= Tmiss:
            
            sInd, t = NewStateSample(stateInd)
            time += t
            
            if time >= Tmiss:
                break
            stateInd = sInd
           
            # Correction du biais lorsqu'une défaillance est forcée
            if time >= Tbias and stateInd != 5:
                stateInd = 5  # Forcer la défaillance
                weight *= np.exp(Lambda_bias * (time-Tbias))

                Tbias = Tbias + time

            if stateInd == 5 and Reliable: 
                weighted_unreliable.append(weight)
                Reliable = False

        # Vérifier l'état final
        if stateInd == 5:
            weighted_unavailable.append(weight)
        else:
            weighted_unavailable.append(0)
        if Reliable:
            weighted_unreliable.append(0)
        weights.append(weight)
    
    return np.array(weighted_unreliable), np.array(weighted_unavailable), np.array(weights)

# Fonction d'estimation de l'erreur
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

    return SE

# Affichage des résultats
plt.figure(figsize=(10, 6))

for Tbias, color in zip(Tbias_values, colors):
    Lambda_bias = Lambda  # Utiliser le taux de défaillance comme biais
    unreliability_values = []
    unavailability_values = []
    
    for Tmiss in Tmiss_values:
        u_reliable, u_available, weights = Unreliability(NumberSim, Tmiss, Tbias, Lambda_bias)
        unreliability_values.append(np.sum(u_reliable)/NumberSim)
        unavailability_values.append(np.sum(u_available)/NumberSim)
    
    # Création des courbes pour chaque Tbias
    plt.plot(Tmiss_values, unreliability_values, label=f"Unreliability (Tbias = {Tbias})", color=color)
    plt.plot(Tmiss_values, unavailability_values, '--', label=f"Unavailability (Tbias = {Tbias})", color=color)

# Configuration du graphique
plt.title("Evolution of Unreliability and Unavailability with Bias Correction")
plt.xlabel("Tmiss")
plt.ylabel("Probability")
plt.legend()
plt.grid()
plt.show()


# Calcul des erreurs pour chaque Tbias
error_values_r = []
error_values_a = []
for Tbias in Tbias_values:
    Lambda_bias = Lambda  # Utiliser le taux de défaillance comme biais
    error_for_Tbias_r = []
    error_for_Tbias_a = []
    
    for Tmiss in Tmiss_values:
        u_reliable, u_available, weights = Unreliability(NumberSim, Tmiss, Tbias, Lambda_bias)
        error_r = compute_accuracy_metrics(u_reliable, weights)
        error_a = compute_accuracy_metrics(u_available, weights)
        error_for_Tbias_r.append(error_r)
        error_for_Tbias_a.append(error_a)
    
    error_values_r.append(error_for_Tbias_r)
    error_values_a.append(error_for_Tbias_a)

# Affichage des résultats
plt.figure(figsize=(10, 6))

for idx, (Tbias, color) in enumerate(zip(Tbias_values, colors)):
    plt.plot(Tmiss_values, error_values_r[idx], label=f"Error (Tbias = {Tbias})", color=color)
    plt.plot(Tmiss_values, error_values_a[idx], '--', label=f"Error (Tbias = {Tbias})", color=color)

# Configuration du graphique
plt.title("Error Comparison between Different Time Bias")
plt.xlabel("Tmiss")
plt.ylabel("Error")
plt.legend()
plt.grid()
plt.show()
