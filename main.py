import graph
import numpy as cu
import pso
import time


def main(graph_path, nr_of_iterations, threads_per_block, blocks_per_grid,nrParticles):
  # nrParticles = 2000
  filename = r'./graphs/graph1000'
  nrNodes, neighborhood, nodes = graph.loadGraph(filename)
  edges = graph.generateEdges(nodes, neighborhood)



  s = time.time()
  pathLen =  pso.pso(nodes, edges, nrParticles, nr_of_iterations, threads_per_block, blocks_per_grid)
  f = time.time()
  return f-s, pathLen


