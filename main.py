import numpy as np
import matplotlib.pyplot as plt


# Constants

crossSection = 1
direction = np.array([1, 0])
numberPoints = 100000

# Step 1 - Draw the initial coordinates and speed of the n from the source density

pos = np.zeros((numberPoints, 2))

i = 0

while i < numberPoints:
    etha = np.random.uniform(0, 1, 1)
    sample = -np.log(etha) / crossSection
    pos[i, :] = pos[i, :] + sample * direction
    i += 1


# Step 2 - Draw it's free flight

# Step 3 - Draw the type of collision

# Step 4 - Deal with next n in memory (if appropriate) and go to 2

# Step 5 - Go to 1 if there are still runs to play

plt.hist(pos[:, 0], bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Position en X')
plt.ylabel('Nombre de points')
plt.title('Distribution des positions en X')
plt.show()
