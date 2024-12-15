from CommonFunctions import *
import matplotlib.pyplot as plt


TotalCrossSection = [0.60, 0.50, 0.40, 0.30]
rng = 100


def ScattAbsorpRatio(TotalCrossSection, ThicknessWall):
    TransProb = []
    VarianceData = []
    numberPoints = 10000
    for i in range(rng):
        ratio = 10**(-2 + 0.04*(i+1))
        print(i)
        SCrossSection = TotalCrossSection/(ratio + 1)
        ACrossSection = TotalCrossSection - SCrossSection
        NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,
                                                                                      SCrossSection, numberPoints)
        TransProb.append(NbPtsTransmitted/numberPoints)



        var = VarianceCalculation(numberPoints, NbPtsTransmitted)
        VarianceData.append(var)
    return TransProb, VarianceData


TransProb = []
VarDat = []

fig, axs = plt.subplots(2, 2,figsize = (18, 11))

fig.suptitle("probability transmission in function of the Absorption/scattering ratio")


for ax, tcs in zip(axs.flat, TotalCrossSection):
    Thickness = 0
    print("AAAAAA")
    ax.set_xscale("log")
    ax.set_title(f"Total cross section ={tcs:.2f} [1/cm] ")
    ax.set_xlabel("Absorption/scattering ratio")
    ax.set_ylabel("probability transmission")
    for i in range(4):
        Thickness += 2.5
        TrsProb, var = ScattAbsorpRatio(tcs, Thickness)
        TransProb.append(TrsProb)
        VarDat.append(var)
        ax.plot([10**(-2 + 0.04*(i+1)) for i in range(rng)], TrsProb, label = f"{Thickness:.2f} cm")
        print(i)
        ax.legend()
print(TransProb)






#plt.plot([0.01*(i + 1) for i in range(99)],TrsProb)
plt.show()









