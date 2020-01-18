import numpy as np
from copy import deepcopy
from graph import norm
import path

CURRENT = 0
BEST = 1

def pso(nodes, edges, nrParticles, nrIterations): 
    currentPaths = path.getRandomPaths(edges, nodes, nrParticles)
    bestPaths = deepcopy(currentPaths)

    particles = np.zeros(shape=(nrParticles,2))
    initParticles(path,particles)

    globalBestPath = getGlobalBestPath(particles,bestPaths[0])
    globalBestCost = countCost(globalBestPath)

    for i in range(nrIterations):
      nextPaths(currentPaths,bestPaths,globalBestPath)
      updateParticles(currentPaths,bestPaths,particles)
      globalBestPath = getGlobalBestPath(particles,globalBestPath,globalBestCost)
    
def initParticles(paths, particles):
    for i in range(len(particles)):
      cost = countCost(paths[i])
      particles[i,CURRENT] = cost
      particles[i,BEST] = cost

def nextPaths(currentPaths,bestPaths,globalBestPath):
  pass

def findNextPath(currentPath,bestPath,globalBestPath):
    maxPathLen = len(currentPath)
    # randomPaths = np.ones(shape=(nrParticles, maxPathLen))*-1
    # randomPaths[:, 0] = 0
    currentNode = 0
    iterator = 1
    while currentNode != 1:
        if iterator >= maxPathLen:
            #zabezpieczenie na wypadek wyjscia poza tablice randomPaths
            iterator = 1
            currentNode = 0
        neighbourNodes = path.getNeighbourNodes(edges, currentNode)
        
        currentNode = getClosestNeighbour(neighbourNodes, bestPath[iterator],globalBestPath[iterator],nodes)

        currentPath[iterator] = currentNode
        iterator += 1


def getClosestNeighbour(neighbourNodes, bestPathNodeIdx,globalBestPathNodeIdx,nodes):
  min([for elem in neighbourNodes])
  # for i in neighbourNodes:

  auto closestNeighbour = neighbours.first;
  auto smallestNorm = GraphGenerator::normSquered(*(*closestNeighbour).second.first,*globalBestPathNode) 
    + GraphGenerator::normSquered(*(*closestNeighbour).second.first,*particelBestPathNode);

  for( auto i =  neighbours.first; i != neighbours.second; ++i)
  {
    auto norm = GraphGenerator::normSquered(*(*i).second.first,*globalBestPathNode) 
        + GraphGenerator::normSquered(*(*i).second.first,*particelBestPathNode);
    if(norm < smallestNorm)
    {
      closestNeighbour = i;
      smallestNorm = norm;
    }
  }
    return (*closestNeighbour).second.first;
}

def sortNodes(neighbourNodes, nodes):
    return sorted(neighbourNodes, key=lambda x: norm(nodes[x], nodes[1]), reverse=False)


#wybrac najlepsza globalnie
#wybrac najlepsza sciezke dla Particle
#porwnac aktulną losową z tymi dwoma
def getGlobalBestPath( particles,globalBestPath, globalBestCost):
    shortestPathIndex = np.argmin(particles[:,1]))
    cost = particles[shortestPathIndex]
    if cost < globalBestCost:
      return paths[shortestPathIndex,:]
    return globalBestPath

def updateParticles(currentPaths,bestPaths,particles):
    for i in range(len(particles)):
        cost = countCost(currentPaths[i])
        updateParticle(currentPaths[i],bestPaths[i],particles[i] ,cost)

def updateParticle(currentPath,bestPath,particle,cost):
    particles[CURRENT] = cost
    if  cost < particles[BEST]:
        bestPaths = deepcopy(currentPaths)
        particles[BEST] = cost


def countCost(path):
    length = 0

    for idx in range(len(path)-1):
        if nodes(path(idx + 1)) == -1:
            return length
        length += norm(nodes[path[idx]],nodes[path[idx + 1]])

    return length