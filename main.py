import numpy as np
import matplotlib.pyplot as plt


# Constants

crossSection = 1
numberPoints = 100000

# Step 1 - Draw the initial coordinates and speed of the n from the source density

pos = np.zeros((numberPoints, 2))
direction = np.zeros((numberPoints, 2))
direction[:, 0] = 1
print(direction)
i = 0

while i < numberPoints:
    etha = np.random.uniform(0, 1, 1)
    theta = np.random.uniform(0, 2 * np.pi, 1)[0]
    direction[i, :] = [np.cos(theta), np.sin(theta)]
    sample = -np.log(etha) / crossSection
    pos[i, :] = pos[i, :] + sample * direction[i, :]
    i += 1


# Step 2 - Draw it's free flight

# Step 3 - Draw the type of collision

# Step 4 - Deal with next n in memory (if appropriate) and go to 2

# Step 5 - Go to 1 if there are still runs to play

x_limits = (0, 0.2)
y_limits = (-0.2, 0.2)

plt.hist2d(pos[:, 0], pos[:, 1], bins=100, range=[x_limits, y_limits], cmap='viridis')

plt.colorbar(label='Densité des points')
plt.xlabel('Position en X')
plt.ylabel('Position en Y')
plt.title('Répartition des points dans le plan')
plt.show()
