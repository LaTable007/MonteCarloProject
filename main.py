import numpy as np
import matplotlib.pyplot as plt


# Constants

crossSectionAbsorp = 0.15
crossSectionScatter = 0.85
numberPoints = 10000
thicknessWall = 2.5

# Step 1 - Draw the initial coordinates and speed of the n from the source density

pos = np.zeros((numberPoints, 2))
direction = np.zeros((numberPoints, 2))
direction[:, 0] = 1

i = 0
numberAbsorp = 0
numberPointsOutside = 0
numberPointsBackScatter = 0

while numberAbsorp < numberPoints:
    i = 0
    while i < numberPoints:
        if np.all(direction[i, :] == 0):
            i += 1
            continue
        ethaAbsorp = np.random.uniform(0, 1, 1)
        ethaScatter = np.random.uniform(0, 1, 1)
    
        sampleAbsorp = -np.log(ethaAbsorp) / crossSectionAbsorp
        sampleScatter = -np.log(ethaScatter) / crossSectionScatter


        if pos[i, 0] > thicknessWall:
            numberPointsOutside += 1
            numberAbsorp += 1
            print(numberAbsorp)
            direction[i, :] = [0, 0]  # Désactive le point
            i += 1
            continue
        
        if pos[i, 0] < 0:
            numberPointsBackScatter += 1
            numberAbsorp += 1
            print(numberAbsorp)
            direction[i, :] = [0, 0]  # Désactive le point
            i += 1
            continue
        
        if sampleAbsorp < sampleScatter:
            pos[i, :] = pos[i, :] + sampleAbsorp * direction[i, :]
            direction[i, :] = [0, 0]
            numberAbsorp += 1
            print(numberAbsorp)
    
        else:    
            theta = np.random.uniform(0, 2 * np.pi, 1)[0]
            direction[i, :] = [np.cos(theta), np.sin(theta)]
            pos[i, :] = pos[i, :] + sampleScatter * direction[i, :]

        i += 1


print('Number of points: ', numberPoints)
print('Number of points outside: ', numberPointsOutside)
print('Number of points backscattered: ', numberPointsBackScatter)

# Step 2 - Draw it's free flight

# Step 3 - Draw the type of collision

# Step 4 - Deal with next n in memory (if appropriate) and go to 2

# Step 5 - Go to 1 if there are still runs to play

x_limits = (thicknessWall - thicknessWall*1.5, thicknessWall*1.5)
y_limits = (-thicknessWall*1.5, thicknessWall*1.5)

plt.hist2d(pos[:, 0], pos[:, 1], bins=100, range=[x_limits, y_limits], cmap='viridis')
plt.colorbar(label='Densité des points')


plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Début de la région')
plt.axvline(x=thicknessWall, color='red', linestyle='--', linewidth=2, label='Fin de la région')

plt.xlabel('Position en X')
plt.ylabel('Position en Y')
plt.title('Répartition des points dans le plan')
plt.show()
