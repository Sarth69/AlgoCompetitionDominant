import os
import sys

if __name__ == "__main__":
    input_dir = os.path.abspath(sys.argv[1])
    score = 0
    i = 0
    bestScores = [18, 25, 33, 40, 19, 45, 87, 173, 34, 84, 167, 334]
    f = open(input_dir, "r")
    for line in f:
        nodesList = line.split(" ")
        if (i == 0):
            print("Graphes denses")
        elif (i == 4):
            print("Graphes étoiles")
        elif (i == 8):
            print("Graphes chaînes")
        print(nodesList[0] + " " + str(len(nodesList)-1) +
              " / " + str(bestScores[i]))
        score += (len(nodesList) - 1)
        i += 1
    print("Score total : " + str(score))
    f.close()
