# Use:
# python Task2.py Formula_One_1984.wmg
# To run the script

import math
import random
import time
import sys
import json

def costFunctionKemeny(r, raceResultsDic):
    visited = []
    cost = 0 
    for i in r:
        for j in visited:
            if raceResultsDic[i] != None:
                # did someone further down the list beat a person ranked higher
                if j in raceResultsDic[i]:
                    cost = cost + raceResultsDic[i][j]
        visited.append(i)
    return cost


def twoRandomIndexes(numOfParticipants):
    ints = range(0, numOfParticipants - 1)
    return [ints[i] for i in random.sample(ints, 2)]

def twoChangeNeighbourFinder(ranking, numOfParticipants, raceResultsDic, xNowCost):
    # takes a ranking and returns the same ranking but with a random two positions swapped 

    indexes = twoRandomIndexes(numOfParticipants)
    # indexes = [8, 13]
    indexes.sort()

    # swap the two random indexes 
    twoChangeNeighbour = ranking[:]
    p1 = twoChangeNeighbour[indexes[1]]
    p2 = twoChangeNeighbour[indexes[0]]
    twoChangeNeighbour[indexes[0]] = p1
    twoChangeNeighbour[indexes[1]] = p2

    xPrimeCost = 0
    xNowSubListCost = costFunctionKemeny(ranking[indexes[0]:indexes[1]+1], raceResultsDic)
    xPrimeSubListCost = costFunctionKemeny(twoChangeNeighbour[indexes[0]:indexes[1]+1], raceResultsDic)
    
    xPrimeCost = xNowCost - xNowSubListCost + xPrimeSubListCost

    return twoChangeNeighbour, xPrimeCost

def simAnnealing(x0, numOfParticipants, raceResultsDic, TI, TL, a, num_non_improve):
    # Simulated Annealing algorithm
    T = TI
    xNow = x0
    xNowCost = costFunctionKemeny(x0, raceResultsDic)
    currentMinimumCost = xNowCost
    currentMinimum = []
    deltaC = 0
    countSinceLastNewMin = 0

    start = time.time()
    while(countSinceLastNewMin < num_non_improve):
        for j in range(0, TL):

            # check if new ranking beats the current minimum
            if xNowCost < currentMinimumCost:
                currentMinimumCost = xNowCost
                currentMinimum = xNow
                countSinceLastNewMin = 0
            else:
                countSinceLastNewMin = countSinceLastNewMin + 1
            # generate randomly a neighbouring solution
            xPrime, xPrimeCost = twoChangeNeighbourFinder(xNow, numOfParticipants, raceResultsDic, xNowCost)
            # compute change cost
            deltaC = xPrimeCost - xNowCost

            if deltaC <= 0:
                # accept new state
                xNow = xPrime
                xNowCost = xPrimeCost
            else:
                q = random.uniform(0, 1)
                if q < math.e**(-deltaC/T):
                    xNow = xPrime
                    xNowCost = xPrimeCost
        T = a*T
    end = time.time()
    timeTaken = end - start
    return currentMinimum, currentMinimumCost, timeTaken

def organiseRaceResults(raceResults, initalSolution):
    # This function takes the results of the torument and stores them in a dictionary 
    # The id's of the dictionary are the candidates who one. The values is another dictionary
    # where the keys are the can candidates who lost and the values are by how much
    # below is an exsample of 27 beating 32 and 34 by 1 and 2 respectively
    # "27": {
    #     "32": 1,
    #     "34": 2
    # }
    resultsDic = {}
    resultsDic = dict.fromkeys(initalSolution)
    c = 0 
    for raceResult in raceResults:
        if raceResult != '':
            raceResult = raceResult.split(',')
            if resultsDic[int(raceResult[1])] == None:
                resultsDic[int(raceResult[1])] = {int(raceResult[2]): int(raceResult[0])}
            else:
                resultsDic[int(raceResult[1])][int(raceResult[2])] = int(raceResult[0])
    
    # print(json.dumps(resultsDic, sort_keys=True, indent=4))
    return resultsDic

def readFile(fileName):
    # Where the file is read
    f = open(fileName, 'r')
    content = f.read().split('\n')
    numOfParticipants = int(content[0])
    initalSolution = content[1:36]
    howGenerated = content[37]
    raceResults = content[38:]
    playerDic = {}
    for i in initalSolution:
        i = i.strip()
        i = i.split(',')
        playerDic[i[0]] = i[1]
    f.close()
    return playerDic, numOfParticipants, raceResults


if len(sys.argv) == 2:
    playerDic, numOfParticipants, raceResults = readFile(str(sys.argv[1]))
else:
    print('Please add a file name as an argument. e.g. python3 Task2.py Formula_One_1984.wmg')

initalSolution = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

raceResultsDic = organiseRaceResults(raceResults, initalSolution)

# Below is where the simulated annealing function is called 
TI = 1
TL = 9000
a = 0.825
num_non_improve = 9000

bestMinimumFound, bestMinimumFoundCost, timeTaken = simAnnealing(initalSolution, numOfParticipants, raceResultsDic, TI, TL, a, num_non_improve)

print('')
print('Lowest Kemeny score found: ' + str(bestMinimumFoundCost))
print('timeTaken: ' + str(round(timeTaken, 3)))
print("{:<8} {:<20} ".format('Position','Candidate'))

for count, i in enumerate(bestMinimumFound):
    print('-----------------------------')
    print("{:>6} {:>20} ".format(str(count+1), playerDic[str(i)]))




