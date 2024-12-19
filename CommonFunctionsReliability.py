import numpy as np


def SejournTimeSample(StateInd, A):
    etha = np.random.uniform(0, 1)
    return -np.log(etha) / np.abs(A[StateInd][StateInd])

def NewStateSample(StateInd, A):
    etha = np.random.uniform(0, 1)
    P0 = 0
    P1 = 0  # noah repond j'ai fait une connerie hahah
    state = 0
    for i in range(len(A)):
        if i == StateInd: continue
        P1 += A[StateInd][i] / np.abs(A[StateInd][StateInd])
        if P0 <= etha < P1:
            state = i
            break
        P0 += A[StateInd][i] / np.abs(A[StateInd][StateInd])
    return state

def Unreliability(numberSim, Tmiss, A):
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
            time += SejournTimeSample(stateInd, A)
            if time >= Tmiss: break
            stateInd = NewStateSample(stateInd, A)
            #print(stateInd)
            if stateInd == 5 and Reliable:
                numberUnreliableStates += 1
                Reliable = False

        if stateInd == 5:
            numberUnavailableStates += 1
    return numberUnreliableStates, numberUnavailableStates

def NegExponential(time, A, StateInd, sInd):
    return np.abs(A[StateInd][sInd])*np.exp(-np.abs(A[StateInd][sInd])*time)

def UnreliabilityBias(numberSim, Tmiss, A, A_Primme):
    numberUnreliableStates = 0
    numberUnavailableStates = 0
    UnavailableWeights = []
    UnreliableWeights = []
    # on va faire un nombre n fois l'evolution du systeme
    for i in range(numberSim):
        # etat initial du systeme : la unit 1 operationel (1), les 2 autres en cold stand-by (2)
        time = 0
        stateInd = 0
        Reliable = True
        weight = 1

        while time <= Tmiss:
            # sample de la durée pendant laquel il n'y a pas d'evolution du système
            #t = SejournTimeSample(stateInd, A_Primme)
            #time += t*NegExponential(t, A, stateInd)/NegExponential(t, A_Primme, stateInd)
            t = SejournTimeSample(stateInd, A)
            time += t
            #weight *= NegExponential(t, A, stateInd, stateInd)/NegExponential(t, A_Primme, stateInd, stateInd)
            if time >= Tmiss : break
            PreviousStateInd = stateInd
            stateInd = NewStateSample(stateInd, A_Primme)
            weight *= (A[PreviousStateInd][stateInd]/A[PreviousStateInd][PreviousStateInd])/(A_Primme[PreviousStateInd][stateInd]/A_Primme[PreviousStateInd][PreviousStateInd])

            if stateInd == 5 and Reliable:
                numberUnreliableStates += weight
                UnreliableWeights.append(weight)
                Reliable = False

        if stateInd == 5:
            numberUnavailableStates += weight
            UnavailableWeights.append(weight)
    return numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights

def ErrorEstimation(ScatteredWeights, numberPoints, numberPointsTransmitted):
    var = 0
    for weight in ScatteredWeights:
        var += weight**2

    var = var/numberPoints - (numberPointsTransmitted/numberPoints)**2
    return (var/numberPoints)**(1/2)

def VarianceCalculation(TotalNumberNeutrons, TransmittedNeutrons):
    var = TransmittedNeutrons/TotalNumberNeutrons - (TransmittedNeutrons/TotalNumberNeutrons)**2
    return (var/TotalNumberNeutrons)**(1/2)

def UnreliabilityCompBias(numberSim, Tmiss, A, A_Primme):
    numberUnreliableStates = 0
    numberUnavailableStates = 0
    UnavailableWeights = []
    UnreliableWeights = []
    # on va faire un nombre n fois l'evolution du systeme
    for i in range(numberSim):
        # etat initial du systeme : la unit 1 operationel (1), les 2 autres en cold stand-by (2)
        time = 0
        stateInd = 0
        Reliable = True
        weight = 1

        while time <= Tmiss:
            # sample de la durée pendant laquel il n'y a pas d'evolution du système
            sInd, t = BiasedStateSampleEventBased(stateInd, A, A_Primme)
            time += t*NegExponential(t, A, stateInd, sInd) / NegExponential(t, A_Primme, stateInd, sInd)
            if time >= Tmiss: break
            #weight*= NegExponential(t, A, stateInd, sInd) / NegExponential(t, A_Primme, stateInd, sInd)
            stateInd = sInd
            if stateInd == 5 and Reliable:
                numberUnreliableStates += weight
                UnreliableWeights.append(weight)
                Reliable = False

        if stateInd == 5:
            numberUnavailableStates += weight
            UnavailableWeights.append(weight)
    return numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights

def NewStateSampleEventBased(StateInd, A):
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

def BiasedStateSampleEventBased(StateInd, A, A_Primme):
    times = []
    indices = []
    for i in range(len(A_Primme)):
        if i == StateInd or A_Primme[StateInd][i] == 0 : continue
        etha = np.random.uniform(0, 1)
        v = -np.log(etha)/np.abs(A_Primme[StateInd][i])
        times.append(v)
        indices.append(i)
    mint = min(times)
    ind = times.index(mint)

    return indices[ind], times[ind]

def UnreliabilityFFSystemBased(numberSim, Tmiss, A):
    numberUnreliableStates = 0
    numberUnavailableStates = 0
    UnreliableWeights = []
    UnavailableWeights = []
    # on va faire un nombre n fois l'evolution du systeme
    for i in range(numberSim):
        # etat initial du systeme : la unit 1 operationel (1), les 2 autres en cold stand-by (2)
        weight = 1
        T_FF = 1.4*Tmiss
        time = 0
        stateInd = 0
        Reliable = True
        #print(i)

        while time <= Tmiss:
            # sample de la durée pendant laquel il n'y a pas d'evolution du système
            if Reliable:
                t = SejournSampleTimeBiased(stateInd, A, T_FF)
                wght = 1 - np.exp(-np.abs(A[stateInd][stateInd])*T_FF)
            else :
                t = SejournTimeSample(stateInd, A)
                wght = 1
            #print(Tmiss - time, wght)
            weight *= wght
            time += t
            if time >= Tmiss: break
            stateInd = NewStateSample(stateInd, A)
            if stateInd == 5 and Reliable:
                numberUnreliableStates += weight
                UnreliableWeights.append(weight)

                Reliable = False

        if stateInd == 5:
            numberUnavailableStates += weight
            UnavailableWeights.append(weight)

    return numberUnreliableStates, numberUnavailableStates, UnreliableWeights, UnavailableWeights


def SejournSampleTimeBiased(stateInd, A, T):
    etha = np.random.uniform(0, 1)
    wght = 1 - np.exp(-np.abs(A[stateInd][stateInd])*T)
    SampleTime = -np.log(1 - wght * etha)/np.abs(A[stateInd][stateInd])
    return SampleTime

def SejournSampleTimeBiased2(stateInd, A, T):
    etha = np.random.uniform(0, 1)
    Wght = np.exp(-np.abs(A[stateInd][stateInd])*T)
    #Wght =
    print(Wght)
    SampleTime = -np.log(1 - etha*Wght)/np.abs(A[stateInd][stateInd])
    #SampleTime = -np.log(etha)/np.abs(A[stateInd][stateInd])
    return SampleTime, Wght





