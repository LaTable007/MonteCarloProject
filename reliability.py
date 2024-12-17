#On fait d'abord une partie unreliability ce sera plus simple dans un premier temp
#en system based-approach
import numpy as np

seed = 1
np.random.seed(seed)

Lambda_1 = 1
Lambda = 1
Tmiss = 20

# 1 = operating, 0 = failed, 2 = stand-by
possible_states = [[1, 2, 2], [0, 1, 2],[0, 0, 1],[0, 0, 0]]
#on garde l'ordre dans choisi dans possible states pour donner un numero à chauqe état pour pouvoir les identifier dans le code
A = [[-Lambda_1, Lambda_1, 0, 0], [0, -Lambda, Lambda, 0], [0, 0, -Lambda, Lambda],[0, 0, 0, 0]]
failed_state = [0, 0, 0]
numberSim = 10000

def SejournTimeSample(StateInd):
    etha = np.random.uniform(0, 1)
    return -np.log(etha)/np.abs(A[StateInd][StateInd])

def NewStateSample(StateInd):
    etha = np.random.uniform(0, 1)
    P0 = 0
    P1 = 0
    state = 0
    for i in range(len(A)):
        if i == StateInd : continue
        P1 += A[stateInd][i]/np.abs(A[StateInd][StateInd])
        if P0 <= etha < P1:
            state = i 
            break
        P0 += A[stateInd][i]/np.abs(A[StateInd][StateInd])
    return state




numberFailedStates = 0
# on va faire un nombre n fois l'evolution du systeme
for i in range(numberSim):
    #etat initial du systeme : la unit 1 operationel (1), les 2 autres en cold stand-by (2)
    time = 0
    stateInd = 0

    while stateInd != 3:
        #sample de la durée pendant laquel il n'y a pas d'evolution du système
        time += SejournTimeSample(stateInd)
        if time >= Tmiss : break
        stateInd = NewStateSample(stateInd)
        if stateInd == 3:
            numberFailedStates += 1


print(numberFailedStates/numberSim)
    
        
    


        #il faut d'abord identifier dans le code chaque état possible => j'envoie le state graph dans le groupe

