import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import combinations
np.random.seed(0)
white_points = np.random.rand(150, 2)
black_points = np.random.rand(150, 2)
np.random.shuffle(black_points)
assert len(white_points) == 150
assert len(black_points) == 150
edges = [(white_points[i], black_points[i]) for i in range(150)]
def plot_edges(ax, edges):
    ax.clear()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')  # Set background to black
    ax.scatter(white_points[:, 0], white_points[:, 1], color='red')
    ax.scatter(black_points[:, 0], black_points[:, 1], color='green')
    for edge in edges:
        ax.plot([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]], 'yellow')  # Yellow connections
    ax.axis('off')
def does_cross(p1, p2, p3, p4):
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)
def resolve_crossings(edges):
    print("Resolving crossings...")
    frames = [edges.copy()]
    crossings = True
    iteration = 0
    while crossings:
        iteration += 1
        print(f"Iteration {iteration}: checking for crossings...")
        crossings = False
        for i, j in combinations(range(len(edges)), 2):
            if does_cross(edges[i][0], edges[i][1], edges[j][0], edges[j][1]):
                print(f"Crossing detected between edges {i} and {j}. Resolving...")
                edges[i], edges[j] = (edges[i][0], edges[j][1]), (edges[j][0], edges[i][1])
                crossings = True
                frames.append(edges.copy())
                break
        frames.append(edges.copy())
        if not crossings:
            print("No more crossings found.")
    return frames
frames = resolve_crossings(edges)

def update(frame_data):
    frame, iteration = frame_data
    plot_edges(ax, frame)

fig, ax = plt.subplots(figsize=(10, 10))

print("Creating animation...")
ani = animation.FuncAnimation(fig, update, frames=[(frame, i) for i, frame in enumerate(frames)], repeat=False)
ani.save('matching_animation.mp4', writer='ffmpeg', fps=20)
print("Animation saved as 'matching_animation.mp4'.")
plt.show()
