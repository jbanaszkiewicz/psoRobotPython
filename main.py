import graph
import cupy as cu
import pso
import time

nrParticles = 200
nrIterations = 10
filename = r'./graphs/graph100'
nrNodes, neighborhood, nodes = graph.loadGraph(filename)
edges = graph.generateEdges(nodes, neighborhood)

memory_pool = cu.cuda.MemoryPool()
cu.cuda.set_allocator(memory_pool.malloc)
pinned_memory_pool = cu.cuda.PinnedMemoryPool()
cu.cuda.set_pinned_memory_allocator(pinned_memory_pool.malloc)

nodes = cu.asarray(nodes)
edges = cu.asarray(edges)
s = time.time()
pso.pso(nodes, edges, nrParticles, nrIterations)
f = time.time()
print(f-s)
##pso search

