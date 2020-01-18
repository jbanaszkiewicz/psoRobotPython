import numpy as np
from copy import deepcopy
from graph import norm
from path import getRandomPaths, getNeighbourNodes

CURRENT = 0
BEST = 1

def pso(nodes, edges, nrParticles, nrIterations): 
    currentPaths = getRandomPaths(edges, nodes, nrParticles)
    bestPaths = deepcopy(currentPaths)

    particles = np.zeros(shape=(nrParticles,2))
    initParticles(bestPaths,particles, nodes)

    globalBestPath = getGlobalBestPath(bestPaths, particles,bestPaths[0], countCost(bestPaths[0], nodes))
    globalBestCost = countCost(globalBestPath, nodes)

    for i in range(nrIterations):
      nextPaths(currentPaths,bestPaths,globalBestPath)
      updateParticles(currentPaths,bestPaths,particles, nodes)
      globalBestPath = getGlobalBestPath(bestPaths, particles,globalBestPath,globalBestCost)
      globalBestCost = countCost(globalBestPath, nodes)
    
def initParticles(paths, particles, nodes):
    for i in range(len(particles)):
      cost = countCost(paths[i], nodes)
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
        neighbourNodes = getNeighbourNodes(edges, currentNode)
        
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
    shortestPathIndex = np.argmin(particles[:,BEST])
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
        bestPath = deepcopy(currentPath)
        particle[BEST] = cost


def countCost(path, nodes):
    length = 0

    for idx in range(len(path)-1):
        if path[idx + 1] == -1:
            return length
        length += norm(nodes[path[idx]],nodes[path[idx + 1]])

    return length