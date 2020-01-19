import numpy as cu
# import cupy
from numba import cuda, types
from numba.cuda.random import create_xoroshiro128p_states

import numba as nb
from path import getRandomPaths, setNeighbourNodes
from math import sqrt

CURRENT = int(0)
BEST = int(1)

@cuda.jit
def add_kernel(x, y, out):
    tx = cuda.threadIdx.x # this is the unique thread ID within a 1D block
    ty = cuda.blockIdx.x  # Similarly, this is the unique block ID within the 1D grid

    block_size = cuda.blockDim.x  # number of threads per block
    grid_size = cuda.gridDim.x    # number of blocks in the grid
    
    start = tx + ty * block_size
    stride = block_size * grid_size

    # assuming x and y inputs are same length
    for i in range(start, x.shape[0], stride):
        out[i] = x[i] + y[i]

def pso(nodes_h, edges_h, nrParticles, nrIterations): 
    nodes = cuda.to_device(nodes_h)
    edges = cuda.to_device(edges_h)
    cuda.synchronize()
    
    threads_per_block = 128
    blocks_per_grid = 30

    currentPaths = cuda.device_array(shape=(nrParticles, len(nodes)), dtype=int)
    neighbourNodes = cuda.device_array(shape=(nrParticles, len(nodes)), dtype=int)
    rng_states = create_xoroshiro128p_states(threads_per_block * blocks_per_grid, seed=1)
    getRandomPaths[blocks_per_grid, threads_per_block](edges, nodes, nrParticles,currentPaths,neighbourNodes,rng_states)

    bestPaths = cuda.to_device(cu.copy(currentPaths)) # copy on gpu
    cuda.synchronize()

    particles = cuda.to_device(cu.zeros(shape=(nrParticles,2)))
    initParticles[blocks_per_grid, threads_per_block](bestPaths,particles, nodes)
    cuda.synchronize()

    # globalBestPath = getGlobalBestPath(bestPaths, particles,bestPaths[0], countCost(bestPaths[0], nodes))
    # globalBestCost = countCost(globalBestPath, nodes)

    # for i in range(nrIterations):
    #   nextPaths(currentPaths,bestPaths,globalBestPath)
    #   updateParticles(currentPaths,bestPaths,particles, nodes)
    #   globalBestPath = getGlobalBestPath(bestPaths, particles,globalBestPath,globalBestCost)
    #   globalBestCost = countCost(globalBestPath, nodes)
    
@cuda.jit
def initParticles(paths, particles, nodes):
    tx = cuda.threadIdx.x # this is the unique thread ID within a 1D block
    ty = cuda.blockIdx.x  # Similarly, this is the unique block ID within the 1D grid

    block_size = cuda.blockDim.x  # number of threads per block
    grid_size = cuda.gridDim.x    # number of blocks in the grid
    
    start = tx + ty * block_size
    stride = block_size * grid_size

    for i in range(start, particles.shape[0], stride):
      cost = countCost(paths[i], nodes)
      particles[i,CURRENT] = cost
      particles[i,BEST] = cost

def nextPaths(currentPaths,bestPaths,globalBestPath):
  pass

def findNextPath(currentPath,bestPath,globalBestPath):
    maxPathLen = len(currentPath)
    # randomPaths = cu.ones(shape=(nrParticles, maxPathLen))*-1
    # randomPaths[:, 0] = 0
    currentNode = 0
    iterator = 1
    while currentNode != 1:
        if iterator >= maxPathLen:
            #zabezpieczenie na wypadek wyjscia poza tablice randomPaths
            iterator = 1
            currentNode = 0
        # TODO teraz sąsiedzi są globalni trzeba rozważyć
        # setNeighbourNodes(edges, currentNode)
        
        # currentNode = getClosestNeighbour(neighbourNodes, bestPath[iterator],globalBestPath[iterator],nodes)

        currentPath[iterator] = currentNode
        iterator += 1


# def getClosestNeighbour(neighbourNodes, bestPathNodeIdx,globalBestPathNodeIdx,nodes):
#   min([for elem in neighbourNodes])
#   # for i in neighbourNodes:

#   auto closestNeighbour = neighbours.first;
#   auto smallestNorm = GraphGenerator::normSquered(*(*closestNeighbour).second.first,*globalBestPathNode) 
#     + GraphGenerator::normSquered(*(*closestNeighbour).second.first,*particelBestPathNode);

#   for( auto i =  neighbours.first; i != neighbours.second; ++i)
#   {
#     auto norm = GraphGenerator::normSquered(*(*i).second.first,*globalBestPathNode) 
#         + GraphGenerator::normSquered(*(*i).second.first,*particelBestPathNode);
#     if(norm < smallestNorm)
#     {
#       closestNeighbour = i;
#       smallestNorm = norm;
#     }
#   }
#     return (*closestNeighbour).second.first;
# }

def sortNodes(neighbourNodes, nodes):
    return sorted(neighbourNodes, key=lambda x: norm(nodes[x], nodes[1]), reverse=False)


#wybrac najlepsza globalnie
#wybrac najlepsza sciezke dla Particle
#porwnac aktulną losową z tymi dwoma

def getGlobalBestPath(paths, particles,globalBestPath, globalBestCost):
    # zrownoleglic jak będzie na gpu
    shortestPathIndex = cu.argmin(particles[:,BEST])
    cost = particles[shortestPathIndex, BEST]
    if cost < globalBestCost:
      return paths[shortestPathIndex,:]
    return globalBestPath

def updateParticles(currentPaths,bestPaths,particles, nodes):
    for i in range(len(particles)):
        cost = countCost(currentPaths[i], nodes)
        updateParticle(currentPaths[i],bestPaths[i],particles[i] ,cost)

def updateParticle(currentPath,bestPath,particle,cost):
    particle[CURRENT] = cost
    if  cost < particle[BEST]:
        bestPath = cu.copy(currentPath)

        particle[BEST] = cost

@cuda.jit(device=True)
def countCost(path, nodes):
    length = float(0)

    for idx in range(len(path)-1):
        if path[idx + 1] == -1:
            return length
        p = nodes[int(path[idx])]
        q = nodes[int(path[idx + 1])]
        length += float(sqrt((p[0] - q[0])*(p[0] - q[0]) + (p[1] - q[1])*(p[1] - q[1])))

    return float(length)


# @cuda.jit(device=True)
# def norm(p, q):
#     return cu.square((p[0] - q[0])*(p[0] - q[0]) + (p[1] - q[1])*(p[1] - q[1]))
