import numpy as np
import matplotlib.pyplot as plt
import pickle

N = np.load("agents.npy")
n = 2

sequence = {}
local_function = {}
for i in range(N):
    filename = "agent_{}_sequence.npy".format(i)
    sequence[i] = np.load(filename)
    with open('agent_{}_function.pkl'.format(i), 'rb') as inp:
        local_function[i] = pickle.load(inp)

plt.figure()
colors = {}
for i in range(N):
    colors[i] = np.random.rand(3, 1).flatten()
    dims = sequence[i].shape
    print(dims)
    iterations = dims[0]
    for j in range(dims[1]):
        plt.plot(np.arange(iterations), sequence[i][:, j, 0], color=colors[i])

function = np.zeros([iterations, 1])
for k in range(iterations):
    avg = np.zeros([n, 1])
    for i in range(N):
        avg += sequence[i][k, :, 0].reshape(n, 1)
    avg = avg/N
    for i in range(N):
        function[k] += local_function[i].eval(avg).flatten()

plt.figure()
plt.semilogy(function)

plt.show()
