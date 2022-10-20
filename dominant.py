import sys
import os
import time
import networkx as nx


def getNewDominantNode(g, uncoveredNodes):
    nodeThatCoversMax = uncoveredNodes[0]
    nodesCoveredMax = 0
    nodesThisNodeWouldCover = [1 for n in g.nodes]
    for e in g.edges:
        if (int(e[0]) in uncoveredNodes and int(e[1]) in uncoveredNodes):
            nodesThisNodeWouldCover[int(e[0])] += 1
            if (nodesCoveredMax < nodesThisNodeWouldCover[int(e[0])]):
                nodesCoveredMax = nodesThisNodeWouldCover[int(e[0])]
                nodeThatCoversMax = int(e[0])
            nodesThisNodeWouldCover[int(e[1])] += 1
            if (nodesCoveredMax < nodesThisNodeWouldCover[int(e[1])]):
                nodesCoveredMax = nodesThisNodeWouldCover[int(e[1])]
                nodeThatCoversMax = int(e[1])
    return nodeThatCoversMax


def getNewDominantNodeInPossibleNodes(g, uncoveredNodes, newPossibleNodes):
    nodeThatCoversMax = newPossibleNodes[0]
    nodesCoveredMax = 0
    for node in newPossibleNodes:
        numberOfNeighborsUncovered = len(
            [n for n in g.neighbors(str(node)) if n in uncoveredNodes])
        if (nodesCoveredMax < numberOfNeighborsUncovered):
            nodesCoveredMax = numberOfNeighborsUncovered
            nodeThatCoversMax = int(node)
    return nodeThatCoversMax


def dominant(g):
    """
        A Faire:
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html
    """
    ts = time.time()
    graphSize = g.order()
    dominant = []
    uncoveredNodes = [n for n in range(graphSize)]
    possibleNewDoms = []
    # We choose a first node
    # Then, we look in its neighbors for a new node to add
    # Each time, we choose the one that add the most nodes in the covered set
    newDom = getNewDominantNode(g, uncoveredNodes)
    uncoveredNodes.remove(newDom)
    dominant.append(newDom)
    for node in g.neighbors(str(newDom)):
        uncoveredNodes.remove(int(node))
        possibleNewDoms.append(int(node))
    while(len(uncoveredNodes) > 0):
        newDom = getNewDominantNodeInPossibleNodes(
            g, uncoveredNodes, possibleNewDoms)
        dominant.append(newDom)
        possibleNewDoms.remove(newDom)
        for node in g.neighbors(str(newDom)):
            if (int(node) in uncoveredNodes):
                uncoveredNodes.remove(int(node))
            if (int(node) not in dominant and int(node) not in possibleNewDoms):
                possibleNewDoms.append(int(node))

    # We elagate the dominant set
    reducedDominant = [False for n in range(graphSize)]
    for i in dominant:
        reducedDominant[i] = True
    i = 0
    for i in dominant:
        # We try to remove the dominant i
        reducedDominant[i] = False
        covered = [False for n in range(graphSize)]
        numberOfCovered = 0
        # The dominants are dominated
        for node in range(graphSize):
            if(reducedDominant[node]):
                covered[node] = True
                numberOfCovered += 1
        # Their neighbors too
        for e in g.edges:
            if (reducedDominant[int(e[0])] and not covered[int(e[1])]):
                covered[int(e[1])] = True
                numberOfCovered += 1
            elif (reducedDominant[int(e[1])] and not covered[int(e[0])]):
                covered[int(e[0])] = True
                numberOfCovered += 1
        if numberOfCovered < graphSize:
            # We can't remove this dominant, so we put it back
            reducedDominant[i] = True
    dominant = [n for n in range(graphSize) if reducedDominant[n]]

    # We get a second dominant set
    uncoveredNodes = [n for n in range(graphSize)]
    dominant2 = []
    while (len(uncoveredNodes) > 0):
        # To get it, we add the node that adds the most covered nodes
        nodeThatCoversMax = getNewDominantNode(g, uncoveredNodes)
        dominant2 += [nodeThatCoversMax]
        uncoveredNodes.remove(nodeThatCoversMax)
        for e in g.edges:
            if (int(e[0]) == nodeThatCoversMax and int(e[1]) in uncoveredNodes):
                uncoveredNodes.remove(int(e[1]))
            elif (int(e[1]) == nodeThatCoversMax and int(e[0]) in uncoveredNodes):
                uncoveredNodes.remove(int(e[0]))

    # # We compare it to a second dominant set
    # # For this one, the criteria will be the difference between the number of neighbors and the mean number of neighbors of the neighbors
    # uncoveredNodes = [n for n in range(graphSize)]
    # dominant2 = []
    # while (len(uncoveredNodes) > 0):
    #     # To get it, we add the node that adds the most covered nodes
    #     nodesThisNodeWouldCover = [[n] for n in g.nodes]
    #     # We compute the number of nodes each new dom would add
    #     for e in g.edges:
    #         if (int(e[0]) in uncoveredNodes and int(e[1]) in uncoveredNodes):
    #             nodesThisNodeWouldCover[int(e[0])] += [int(e[1])]
    #             nodesThisNodeWouldCover[int(e[1])] += [int(e[0])]

    #     # We get the node maximizing the score
    #     maxScore = -graphSize ^ 2
    #     nodeMaximizingScore = uncoveredNodes[0]
    #     for node in uncoveredNodes:
    #         score = len(nodesThisNodeWouldCover[node])
    #         # We reduce the score by the average of neighbors of the neighbors of the node
    #         average = 0
    #         for neighbor in nodesThisNodeWouldCover[node]:
    #             average += len(nodesThisNodeWouldCover[int(neighbor)]) - 1
    #         if (score > 0):
    #             average /= score

    #         # We update the max accordingly
    #         if (score - average) > maxScore:
    #             maxScore = score-average
    #             nodeMaximizingScore = node

    #     # We add the best node to the dominant
    #     dominant2 += [nodeMaximizingScore]
    #     uncoveredNodes.remove(nodeMaximizingScore)
    #     for e in g.edges:
    #         if (int(e[0]) == nodeMaximizingScore and int(e[1]) in uncoveredNodes):
    #             uncoveredNodes.remove(int(e[1]))
    #         elif (int(e[1]) == nodeMaximizingScore and int(e[0]) in uncoveredNodes):
    #             uncoveredNodes.remove(int(e[0]))

    # We choose the best dominant of the 2 computed
    if (len(dominant) > len(dominant2)):
        dominant = dominant2

    # # We check if we can remove a node from the dominant set found
    # reducedDominant = [False for n in range(graphSize)]
    # for i in dominant:
    #     reducedDominant[i] = True
    # i = 0
    # for i in dominant:
    #     # We try to remove the dominant i
    #     reducedDominant[i] = False
    #     covered = [False for n in range(graphSize)]
    #     numberOfCovered = 0
    #     # The dominants are dominated
    #     for node in range(graphSize):
    #         if(reducedDominant[node]):
    #             covered[node] = True
    #             numberOfCovered += 1
    #     # Their neighbors too
    #     for e in g.edges:
    #         if (reducedDominant[int(e[0])] and not covered[int(e[1])]):
    #             covered[int(e[1])] = True
    #             numberOfCovered += 1
    #         elif (reducedDominant[int(e[1])] and not covered[int(e[0])]):
    #             covered[int(e[0])] = True
    #             numberOfCovered += 1
    #     if numberOfCovered < graphSize:
    #         # We can't remove this dominant, so we put it back
    #         reducedDominant[i] = True
    #     else:
    #         print("removed a dom")
    print("Execution time : " + str(time.time() - ts))
    return dominant


#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__ == "__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(input_dir, "doesn't exist")
        exit()

    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(
        time.strftime("%d%b%Y_%H%M%S", time.localtime()))
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for graph_filename in sorted(os.listdir(input_dir)):
        # print(graph_filename)
        # importer le graphe
        g = nx.read_adjlist(os.path.join(input_dir, graph_filename))

        # calcul du dominant
        D = sorted(dominant(g), key=lambda x: int(x))

        # ajout au rapport
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
        output_file.write('\n')

    output_file.close()
