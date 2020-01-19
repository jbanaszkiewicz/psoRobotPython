import numpy as cu
import cupy
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
    cuda.synchronize()

    getRandomPaths[blocks_per_grid, threads_per_block](edges, nodes, nrParticles,currentPaths,neighbourNodes,rng_states)
    cuda.synchronize()
    
    bestPaths = cuda.to_device(cu.copy(currentPaths)) # copy on gpu
    cuda.synchronize()

    particles = cuda.device_array(shape=(nrParticles,2), dtype=float)
    cuda.synchronize()

    initParticles[blocks_per_grid, threads_per_block](bestPaths,particles, nodes)
    cuda.synchronize()

    globalBestPath = cuda.device_array(shape=(1, bestPaths.shape[1]), dtype=int)
    shortestGlobalIdx = getGlobalBestPath(particles, particles[0, BEST])
    if shortestGlobalIdx != -1:
      globalBestPath[0, :] = bestPaths[shortestGlobalIdx, :]
    
    globalBestCost = particles[shortestGlobalIdx, BEST]


    for i in range(nrIterations):
      nextPaths(currentPaths,bestPaths,globalBestPath, neighbourNodes)
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


@cuda.jit
def getNewPaths(currentPaths, bestPaths, globalBestPath, neighbourNodes, nodes ):
  tx = cuda.threadIdx.x # this is the unique thread ID within a 1D block
  ty = cuda.blockIdx.x  # Similarly, this is the unique block ID within the 1D grid

  block_size = cuda.blockDim.x  # number of threads per block
  grid_size = cuda.gridDim.x    # number of blocks in the grid
  
  start = tx + ty * block_size
  stride = block_size * grid_size
  for i in range(start, currentPaths.shape[0], stride):
    getNewPath(currentPaths[i], bestPaths[i], globalBestPath, neighbourNodes[i], nodes)


@cuda.jit(device=True)
def getNewPath(currentPath, bestPath, globalBestPath, neighbourNodes, nodes):
  
  
  for i, localBest, globalBest, idxsNgbr in enumerate(zip(bestPath, globalBestPath, neighbourNodes)):
    if 
    idx = findBestNeighbour(nodes[localBest], nodes[globalBest], idxsNgbr, nodes)
    currentPath[i] = idx 
  


@cuda.jit(device=True)
def findBestNeighbour(bestPathNode,globalBestPathNode, neighboursNode, nodes):
  """
  Funkcja zdanduje najlepszy nowy wezel
  bestPathNode :param: type Node
  globalBestPathNode :param: type Node
  neighboursNode :param: table of indexs in nodes, uzupełnione przez -1
  nodes :param: tablica z Nodes
  """
  distance = norm(bestPathNode, nodes[neighboursNode[0]])+ norm(globalBestPathNode, nodes[neighboursNode[0]] )
  idx = neighboursNode[0]
  for ngbr in neighboursNode:
    if neighbourNode[ngbrIdx] >0:
      curDistance = norm(bestPathNode, nodes[ngbr])+ norm(globalBestPathNode, nodes[ngbr] )
      if curDistance < distance:
        distance = curDistance
        idx = ngbr
    else break
  return idx


def sortNodes(neighbourNodes, nodes):
    return sorted(neighbourNodes, key=lambda x: norm(nodes[x], nodes[1]), reverse=False)


#wybrac najlepsza globalnie
#wybrac najlepsza sciezke dla Particle
#porwnac aktulną losową z tymi dwoma

def getGlobalBestPath(particlesN,globalBestCost):
    # zrownoleglic jak będzie na gpu
    particles = cupy.asarray(particlesN)
    shortestPathIndex = cupy.argmin(particles[:,BEST])
    cost = particles[shortestPathIndex, BEST]
    if cost < globalBestCost:
      return int(shortestPathIndex)
    else:
      return -1

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
        length += norm(nodes[int(path[idx])], nodes[int(path[idx + 1])])

    return float(length)



@cuda.jit(device=True)
def norm(p, q):
    return float(sqrt((p[0] - q[0])*(p[0] - q[0]) + (p[1] - q[1])*(p[1] - q[1])))
