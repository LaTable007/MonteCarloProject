from CommonFunctions import *

ACrossSection = 6.98
SCrossSection = 0.08

VarianceData = []
MeanData = []


numberPoints = 1000000

rng = 50


ThicknessWall = 0
TransProb = []
NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,
                                                                                  SCrossSection, numberPoints)
ThicknessWall = 0
print(NbPtsTransmitted/numberPoints)

for i in range(rng):
    print(i)
    ThicknessWall += 0.02
    NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,
                                                                                  SCrossSection, numberPoints)
    TransProb.append(NbPtsTransmitted/numberPoints)
    var = VarianceCalculation(numberPoints, NbPtsTransmitted)
    VarianceData.append(var)




fig, (ax0, ax1) = plt.subplots(1, 2, figsize = (16, 6))


ax0.plot([0.02*(i + 1) for i in range(rng)], TransProb)
ax0.set_yscale("log")
ax0.set_xlabel('Wall Thickness [cm]')
ax0.set_ylabel('Transmission Probability')
ax0.axhline(y=1E-3, color='red', linestyle='--', linewidth=1)
ax0.set_title("""Transmission Probability in function of the Wall's thickness""")



ax1.plot([0.02*(i + 1)  for i in range(rng)], VarianceData)
ax1.set_yscale("log")
ax1.set_xlabel('wall Thickness [cm]')
ax1.set_ylabel('Relative Error')
ax1.set_title(""" Standard error estimation""")
plt.show()














