import graph
import path



nrParticles = 2
filename = r'./graphs/graph100'
nrNodes, neighborhood, nodes = graph.loadGraph(filename)
edges = graph.generateEdges(nodes, neighborhood)
randomPaths = path.getRandomPaths(edges, nodes, nrParticles)

