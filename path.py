import cupy as cu
import random
from graph import norm

def getNeighbourNodes(edges, nodeIdx):
    vector = edges[nodeIdx, :]
    idxs = [idx for idx, elem in enumerate(vector) if elem>=0]
    return idxs


def sortNodes(neighbourNodes, nodes):
    return sorted(neighbourNodes, key=lambda x: norm(nodes[x], nodes[1]), reverse=False)


def getRandomPaths(edges, nodes, nrParticles):
    """
    Sprawdzam, czy w wektorze mam tyle losowych ścieżek, ile jest wymagane.
    Jeśli nie, rozpoczynam tworzenie nowej losowej ścieżki, którą dodam do wektora.

    Sytuacja wygląda tak: funkcja getNeighbours zwraca parę iteratorów
    A chyba miało być tak, że w jakiś sposób dowiaduję się o wszystkich sąsiadach
    I to z nich wybieram lepszą połowę

    Zakładam, że w tym miejscu mam już kilka node'ów sąsiednich, z których mam wylosować
    Sortowanie elementów w wektorze sąsiadów ze względu na kwadrat ich odległości od destination
    """
#   srand(time(NULL));
    maxPathLen = len(nodes)
    randomPaths = cu.ones(shape=(nrParticles, maxPathLen), dtype=int)*-1
    randomPaths[:, 0] = 0
    for i in range(nrParticles):
        currentNode = 0
        iterator = 1
        while currentNode != 1:
            if iterator >= maxPathLen:
                #zabezpieczenie na wypadek wyjscia poza tablice randomPaths
                iterator = 1
                currentNode = 0
            neighbourNodes = getNeighbourNodes(edges, currentNode)
            
            
            sortedNodes = sortNodes(neighbourNodes, nodes)

            # Ustalam liczbę odpowiadającą połowie sąsiadow
            randomNode = random.randint(0, int(len(sortedNodes)/2))
            # Teraz muszę wylosować liczbę z zakresu od 0 do (halfOfNeighbours - 1)
            currentNode = sortedNodes[randomNode]
            # Ustawienie nowego aktualnego węzła i dodanie go do aktualnej ścieżki
            randomPaths[i, iterator] = currentNode
            iterator += 1
  
    return randomPaths