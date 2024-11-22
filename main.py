import numpy as np


# Constants

crossSection = 1
direction = np.array([1, 0])

# Step 1 - Draw the initial coordinates and speed of the n from the source density

pos = np.array([0, 0])
speed = np.array([1, 0])

etha = np.random.uniform(0, 1, 1)
sample = -np.log(etha) / crossSection

pos = pos + sample * direction

print(pos)

# Step 2 - Draw it's free flight

# Step 3 - Draw the type of collision

# Step 4 - Deal with next n in memory (if appropriate) and go to 2

# Step 5 - Go to 1 if there are still runs to play
