from CommonFunctions import *

ACrossSection = 1
SCrossSection = 67

VarianceData = []
MeanData = []

ThicknessWall = 0
numberPoints = 10000



TransProb = []

for i in range(50):
    ThicknessWall += 0.01
    NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,
                                                                                  SCrossSection, numberPoints)
    TransProb.append(NbPtsTransmitted/numberPoints)

numberPoints = 0
ThicknessWall = 0.1
for i in range(50):
    numberPoints += 100
    NbPtsTransmitted, NbPtsBackScattered, FinalPosition = ProbabilityTransmission(ThicknessWall, ACrossSection,
                                                                                  SCrossSection, numberPoints)
    var = VarianceCalculation(numberPoints, NbPtsTransmitted)
    VarianceData.append(var)



fig, (ax0, ax1) = plt.subplots(1, 2, figsize = (12, 6))


ax0.plot([0.01*i for i in range(50)], TransProb)
ax1.plot([100*i for i in range(50)], VarianceData)
ax0.set_xlabel('Wall Thickness [m]')
ax0.set_ylabel('Transmission Probability')
ax0.set_title("""Transmission Probability in function of the Wall's thickness""")

ax1.set_xlabel('Number Of Neutrons')
ax1.set_ylabel('Error Estimation')
ax1.set_title("""Error Estimation in function of the number of neutrons""")





plt.show()















