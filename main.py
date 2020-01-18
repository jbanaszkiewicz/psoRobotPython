import graph
import numpy as cu
import pso
import time

nrParticles = 128
nrIterations = 1
filename = r'./graphs/graph100'
nrNodes, neighborhood, nodes = graph.loadGraph(filename)
edges = graph.generateEdges(nodes, neighborhood)



s = time.time()
pso.pso(nodes, edges, nrParticles, nrIterations)
f = time.time()
print(f-s)


# import numpy as np

# n = 100000
# x = np.arange(n).astype(np.float32)
# y = 2 * x
# out = np.empty_like(x)



# pso.add_kernel[blocks_per_grid, threads_per_block](x, y, out)
# print(out[:10])
##pso search

