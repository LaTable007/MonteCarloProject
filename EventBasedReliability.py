# On fait d'abord une partie unreliability ce sera plus simple dans un premier temp
# en system based-approach
import numpy as np
import matplotlib.pyplot as plt

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
NumberSim = 10000
print("AAAAAA")



def NewStateSample(StateInd):
    times = []
    indices = []
    for i in range(len(A)):
        if i == StateInd or A[StateInd][i] == 0 : continue
        etha = np.random.uniform(0, 1)
        v = -np.log(etha)/np.abs(A[StateInd][i])
        times.append(v)
        indices.append(i)
    mint = min(times)
    #print(times)
    #print(indices)
    #print(mint)
    ind = times.index(mint)
    print(ind)
    return indices[ind], times[ind]


def Unreliability(numberSim, Tmiss):
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

            sInd, t = NewStateSample(stateInd)
            print(stateInd)
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
unreliability_values = []
unavailability_values = []

for Tmiss in Tmiss_values:
    u_reliable, u_available = Unreliability(NumberSim, Tmiss)
    unreliability_values.append(u_reliable / NumberSim)
    unavailability_values.append(u_available / NumberSim)

# Création des plots
#.figure(figsize=(10, 6))
plt.plot(Tmiss_values, unreliability_values, label="Unreliability", color='blue')
plt.plot(Tmiss_values, unavailability_values, label="Unavailability", color='red')
plt.title("Evolution of Unreliability and Unavailability with Tmiss")
plt.xlabel("Tmiss")
plt.ylabel("Probability")
plt.legend()
plt.grid()
plt.show()
 #il faut d'abord identifier dans le code chaque état possible => j'envoie le state graph dans le groupe

