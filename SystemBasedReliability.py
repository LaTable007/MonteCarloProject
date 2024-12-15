# On fait d'abord une partie unreliability ce sera plus simple dans un premier temp
# en system based-approach
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

# 1 = operating, 0 = failed, 2 = stand-by
possible_states = [[1, 2, 2], [0, 1, 2], [0, 0, 1], [0, 0, 0], [1, 2, 0], [1, 0, 0]]
# on garde l'ordre dans choisi dans possible states pour donner un numero à chauqe état pour pouvoir les identifier dans le code
A = [[-Lambda_1, 0, 0, Lambda_1, 0, 0], [Mu, -Mu - Lambda, 0, 0, Lambda_1, 0],
     [0, 2 * Mu, -2 * Mu - Lambda_1, 0, 0, Lambda_1], [Mu_1, 0, 0, -Mu_1 - Lambda, Lambda, 0],
     [0, 0, 0, Mu, -Mu - Lambda, Lambda], [0, 0, Mu_1, 0, 2 * Mu, -Mu_1 - 2 * Mu]]
failed_state = [0, 0, 0]
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

#Mesure du temps d'execution
start_time = time.time()

# Vecteurs pour les différents Tmiss et résultats
Tmiss_values = np.linspace(0.1, 10000, 50)
unreliability_mean = []
unreliability_CI = []
unavailability_mean = []
unavailability_CI = []

for Tmiss in Tmiss_values:
    #print(Tmiss)
    u_reliable, u_available = Unreliability(NumberSim, Tmiss)

    # Calcule la moyenne et l'interval de confiance pour l'unreliability
    mean_reliable = np.mean(u_reliable)
    variance_reliable = np.var(u_reliable)
    SE_reliable = np.sqrt(variance_reliable / NumberSim) # Erreur standard
    CI_reliable = 1.96 * SE_reliable #Interval de confiance de 95%

    # Calcule la moyenne et l'interval de confiance pour l'unavailibility
    mean_available = np.mean(u_available)
    variance_available = np.var(u_available)
    SE_available = np.sqrt(variance_available / NumberSim)
    CI_available = 1.96 * SE_available

    unreliability_mean.append(mean_reliable)
    unreliability_CI.append(CI_reliable)
    unavailability_mean.append(mean_available)
    unavailability_CI.append(CI_available)

#Temps d'éxecution
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total execution time: {elapsed_time:.2f} seconds")



# Création des plots
plt.figure(figsize=(12, 6))
plt.plot(Tmiss_values, unreliability_mean, label="Unreliability", color='blue')
plt.fill_between(Tmiss_values, np.array(unreliability_mean) - np.array(unreliability_CI),
                 np.array(unreliability_mean) + np.array(unreliability_CI), color='blue', alpha=0.3)

plt.plot(Tmiss_values, unavailability_mean, label="Unavailability", color='red')
plt.fill_between(Tmiss_values, np.array(unavailability_mean) - np.array(unavailability_CI),
                 np.array(unavailability_mean) + np.array(unavailability_CI), color='red', alpha=0.3)
plt.title("Evolution of Unreliability and Unavailability with Tmiss")
plt.xlabel("Tmiss")
plt.ylabel("Probability")
plt.legend()
plt.grid()
plt.show()