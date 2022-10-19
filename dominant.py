import sys
import os
import time
import networkx as nx


def dominant(g):
    """
        A Faire:
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html
    """
    uncoveredNodes = [n for n in range(g.order())]
    dominant = []
    while (len(uncoveredNodes) > 0):
        nodeThatCoversMax = uncoveredNodes[0]
        nodesCoveredMax = 1
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
        dominant += [nodeThatCoversMax]
        uncoveredNodes.remove(nodeThatCoversMax)
        for e in g.edges:
            if (int(e[0]) == nodeThatCoversMax and int(e[1]) in uncoveredNodes):
                uncoveredNodes.remove(int(e[1]))
            elif (int(e[1]) == nodeThatCoversMax and int(e[0]) in uncoveredNodes):
                uncoveredNodes.remove(int(e[0]))
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
