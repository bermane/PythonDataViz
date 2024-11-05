# import packages 
import os
import matplotlib.pyplot as plt

# plt
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5,5)
plt.show()

# plot a point
point = (0.5, 0.5)
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5,5)
ax.plot(point[0], point[1], color='green', marker='o')
plt.show()

# plot multiple points
points = [(0.1, 0.5), (0.5, 0.5), (0.9, 0.5)]

# use zip to create list of x and y coordinates
x, y = zip(*points)
print(x)
print(y)

# plot 1
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5,5)
ax.plot(x, y, color='green', marker='o')
plt.show()

# plot 2
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5,5)
ax.plot(x, y, color='green', marker='o', linestyle='None')
plt.show()

# save figure
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5,5)
ax.plot(x, y, color='green', marker='o', linestyle='None')

output_folder = 'output'
output_path = os.path.join(output_folder, 'simple.png')
plt.savefig(output_path)

plt.show()

# plot the following points
point1 = (4, 1) # green triangle
point2 = (3, 4) # red circle

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5, 5)
ax.plot(point1[0], point1[1], color='green', marker='^')
ax.plot(point2[0], point2[1], color='red', marker='o')
plt.show