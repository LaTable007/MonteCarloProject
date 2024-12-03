from CommonFunctions import *
import matplotlib.pyplot as plt


TotalCrossSection = 68


def ScattAbsorpRatio(TotalCrossSection, ThicknessWall):
    TransProb = []
    VarianceData = []
    ratio = 0
    numberPoints = 10000
    for _ in range(99):
        ratio += 1
        ACrossSection = TotalCrossSection/(ratio + 1)
        SCrossSection = TotalCrossSection - ACrossSection
        NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,
                                                                                      SCrossSection, numberPoints)
        TransProb.append(NbPtsTransmitted/numberPoints)



        var = VarianceCalculation(numberPoints, NbPtsTransmitted)
        VarianceData.append(var)
    return TransProb, VarianceData


Thickness = 0.05
TransProb = []
VarDat = []

fig, axs = plt.subplots(1, 1)


for i in range(5):
    Thickness += 0.05
    TrsProb, var = ScattAbsorpRatio(TotalCrossSection, Thickness)
    TransProb.append(TrsProb)
    VarDat.append(var)
    axs.plot([0.01 * (i + 1) for i in range(99)], TransProb[i], label = f"{Thickness:.2f}")
    print(i)
    axs.legend()






#plt.plot([0.01*(i + 1) for i in range(99)],TrsProb)
plt.show()









