
def main(file_input, file_output):
    # read input
    # n = number of players
    # k = number of opponents each player faces
    # value = list tuple of players' info
    n, k, value, avgPlayerScore, minPlayerScore = readInput(file_input)

    #check
    print("avgScore"+str(avgPlayerScore))
    print(value)

    # have a list of all opponent points for each player
    # listOpponent = []  # [ [(score1, 1), (score2, 2)]   ,  [(score2, 2) , (score3, 3) ...]   , ...]
    # listSumScore = []  # [sum1, sum2, sum3, ...]
    listOpponent, listSumScore = initialize(value, k)
    i = 0
    checkedMaxMin = []

    #check
    print(listOpponent)
    # print(listSumScore)

    i = matchScheduling(n, k, listOpponent, listSumScore, avgPlayerScore, minPlayerScore, checkedMaxMin, i)

    # print(listOpponent)
    print(listSumScore)
    print(i)
    # print the list of opponents as a valid solution.
    writeOutput(listOpponent, file_output)


def stopCondition(n, listSumScore, maxIndex, minIndex, avgPlayerScore, minPlayerScore):
    isOver = False
    if n>100:
        if listSumScore[maxIndex]-listSumScore[minIndex] < ((avgPlayerScore/2) + 1 ):
            print(str(listSumScore[maxIndex]-listSumScore[minIndex])+"why"+str(avgPlayerScore/2))    
            isOver = True
    else:
        if listSumScore[maxIndex]-listSumScore[minIndex] < (minPlayerScore + 1 ):
            print(str(listSumScore[maxIndex]-listSumScore[minIndex])+"why"+str(avgPlayerScore/2))    
            isOver = True
        
    if listSumScore[maxIndex] == listSumScore[minIndex]:
        isOver = True
    return isOver


def repeating(listOpponent, index, opponent):
    for other in listOpponent[index]:
        if other[1] == opponent[1]:
            return True
    return False


def calPoint(point, newMaxScore, newMinScore, idealScore, listSumScore, maxIndex, minIndex):
    if newMaxScore > idealScore:
        point += listSumScore[maxIndex] - newMaxScore 
    else:
        point += newMaxScore - listSumScore[minIndex]
    if newMinScore > idealScore:
        point += listSumScore[maxIndex] - newMinScore
    else:
        point += newMinScore - listSumScore[minIndex]
    return point


def matchScheduling(n, k, listOpponent, listSumScore, avgPlayerScore, minPlayerScore, checkedMaxMin, i):
    while (True):
        i+=1 #check number of max-min processed

        maxIndex, minIndex = maxMin(listSumScore,checkedMaxMin) # e.x. [10, 20, 30] min 0 max 2
        checkedMaxMin.insert(0,(maxIndex,minIndex))

        #check
        print("max"+str(maxIndex)+" "+str(listSumScore[maxIndex])+" "+str(listSumScore[minIndex]))
        print(minIndex)

        #Condition to stop
        isFinish = stopCondition(n, listSumScore, maxIndex, minIndex, avgPlayerScore, minPlayerScore)
        if isFinish == True:
            break

        scoreDiff = listSumScore[maxIndex] - listSumScore[minIndex]
        idealScore = (listSumScore[maxIndex] + listSumScore[minIndex])/2
        # print(scoreDiff)

        bestDiff = -1
        indexOpponentMax = -1
        indexOpponentMin = -1
        # an array  [ (score1, 1), ... ]
        # listOpponent[maxIndex] is a list have highest sum of score [(score1, 1), (score2, 2)], opponentMax maybe (score1, 1)
        for opponentMax in listOpponent[maxIndex]:
            # print("check5")
            if opponentMax[1] == (minIndex+1):
                continue
            if repeating(listOpponent, minIndex, opponentMax) == True:
                continue
            
            # print("check2")
            for opponentMin in listOpponent[minIndex]:
                if opponentMin[1] == (maxIndex+1):
                    continue
                if opponentMin[0] < opponentMax[0]:
                    if (opponentMax[0] - opponentMin[0]) > scoreDiff:
                        continue
                    if repeating(listOpponent, maxIndex, opponentMin) == True:
                        continue

                    #new way to evaluate
                    newMaxScore = listSumScore[maxIndex] - opponentMax[0] + opponentMin[0]
                    newMinScore = listSumScore[minIndex] - opponentMin[0] + opponentMax[0]
                    point = 0  #if newMaxScore > oldMaxScore, point is negative, bad effect, oldMaxScore -newMaxScore = score lost 
                    point = calPoint(point, newMaxScore, newMinScore, idealScore, listSumScore, maxIndex, minIndex)

                    #need to check the affected nodes
                    affectedPlayerMax = listOpponent[maxIndex][listOpponent[maxIndex].index(opponentMax)][1] - 1
                    affectedPlayerMin = listOpponent[minIndex][listOpponent[minIndex].index(opponentMin)][1] - 1
                    indexBeChangedMax = -1
                    indexBeChangedMin = -1
                    for opponent in listOpponent[affectedPlayerMax]:
                        if opponent[1] == maxIndex+1:
                            indexBeChangedMax = listOpponent[affectedPlayerMax].index(opponent)
                    for opponent in listOpponent[affectedPlayerMin]:
                        if opponent[1] == minIndex+1:
                            indexBeChangedMin = listOpponent[affectedPlayerMin].index(opponent)

                    if listOpponent[affectedPlayerMax][indexBeChangedMax][1] == affectedPlayerMin + 1:
                        continue
                    if listOpponent[affectedPlayerMin][indexBeChangedMin][1] == affectedPlayerMax + 1:
                        continue
                    
                    if repeating(listOpponent, affectedPlayerMax, listOpponent[affectedPlayerMin][indexBeChangedMin]) == True:
                         continue
                    if repeating(listOpponent, affectedPlayerMin, listOpponent[affectedPlayerMax][indexBeChangedMax]):
                        continue

                    #new way to evaluate
                    idealScoreAffected = (listSumScore[affectedPlayerMax] + listSumScore[affectedPlayerMin])/2
                    newMaxScoreAffected = listSumScore[affectedPlayerMax] - listOpponent[affectedPlayerMax][indexBeChangedMax][0] + listOpponent[affectedPlayerMin][indexBeChangedMin][0]
                    newMinScoreAffected = listSumScore[affectedPlayerMin] - listOpponent[affectedPlayerMin][indexBeChangedMin][0] + listOpponent[affectedPlayerMax][indexBeChangedMax][0]
                    if listSumScore[affectedPlayerMax] > listSumScore[affectedPlayerMin]:
                        point = calPoint(point, newMaxScoreAffected, newMinScoreAffected, idealScoreAffected, listSumScore, affectedPlayerMax, affectedPlayerMin)
                    else:
                        point = calPoint(point, newMaxScoreAffected, newMinScoreAffected, idealScoreAffected, listSumScore, affectedPlayerMin, affectedPlayerMax)

                    if point <= 0:
                        continue

                    if bestDiff == -1:
                        bestDiff = point
                        indexOpponentMax = listOpponent[maxIndex].index(
                            opponentMax)
                        indexOpponentMin = listOpponent[minIndex].index(
                            opponentMin)
                    elif point > bestDiff:
                        bestDiff = point
                        indexOpponentMax = listOpponent[maxIndex].index(
                            opponentMax)
                        indexOpponentMin = listOpponent[minIndex].index(
                            opponentMin)
        # print(str(bestDiff)+" max "+str(indexOpponentMax)+" min "+str(indexOpponentMin))
        if bestDiff != -1:

            # only change affected, not evaluate
            affectedPlayerMax = listOpponent[maxIndex][indexOpponentMax][1] - 1
            affectedPlayerMin = listOpponent[minIndex][indexOpponentMin][1] - 1

            indexBeChangedMax = -1
            indexBeChangedMin = -1

            for opponent in listOpponent[affectedPlayerMax]:
                if opponent[1] == maxIndex+1:
                    indexBeChangedMax = listOpponent[affectedPlayerMax].index(
                        opponent)

            for opponent in listOpponent[affectedPlayerMin]:
                if opponent[1] == minIndex+1:
                    indexBeChangedMin = listOpponent[affectedPlayerMin].index(
                        opponent)

            listSumScore[affectedPlayerMax] = listSumScore[affectedPlayerMax] - \
                listOpponent[affectedPlayerMax][indexBeChangedMax][0] + \
                listOpponent[affectedPlayerMin][indexBeChangedMin][0]
            listSumScore[affectedPlayerMin] = listSumScore[affectedPlayerMin] - \
                listOpponent[affectedPlayerMin][indexBeChangedMin][0] + \
                listOpponent[affectedPlayerMax][indexBeChangedMax][0]

            listSumScore[maxIndex] = listSumScore[maxIndex] - \
                listOpponent[maxIndex][indexOpponentMax][0] + \
                listOpponent[minIndex][indexOpponentMin][0]
            listSumScore[minIndex] = listSumScore[minIndex] - \
                listOpponent[minIndex][indexOpponentMin][0] + \
                listOpponent[maxIndex][indexOpponentMax][0]

            listOpponent[affectedPlayerMax][indexBeChangedMax], listOpponent[affectedPlayerMin][indexBeChangedMin] = listOpponent[
                affectedPlayerMin][indexBeChangedMin], listOpponent[affectedPlayerMax][indexBeChangedMax]

            listOpponent[minIndex][indexOpponentMin], listOpponent[maxIndex][indexOpponentMax] = listOpponent[
                maxIndex][indexOpponentMax], listOpponent[minIndex][indexOpponentMin]
            #print(listOpponent)    
    return i 


def writeOutput(listOpponent, file_output):
    f = open(file_output, 'w')
    for player in listOpponent:
        print(str(listOpponent.index(player)+1)+": ", end=" ")
        for opponent in player:
            f.write(str(opponent[1])+'\n')
            print(str(opponent[1]), end=" ")
        print(" ")
    f.close()


def maxMin(listSumScore, usedList):
    max = listSumScore[0]
    min = listSumScore[0]

    maxIndex = 0
    minIndex = 0

    i = 0
    for score in listSumScore:
        isUsed = False
        if score >= max:
            for used in usedList:
                if used[0] == i:
                    if used[1] == minIndex:
                        isUsed = True
                        break
            if isUsed == False:      
                max = score
                maxIndex = i
        elif score <= min:
            for used in usedList:
                if used[1] == i:
                    if used[0] == maxIndex:
                        isUsed = True
                        break
            if isUsed == False:
                min = score
                minIndex = i
        i += 1

    return maxIndex, minIndex

def readInput(file_input):
    f = open(file_input, 'r')

    firstline = f.readline()
    n, k = firstline.split(" ")
    n = int(n)
    k = int(k)
    # number of players, number of opponents each player faces
    value = []

    avgPlayerScore = 0
    minPlayerScore = -1
    i = 1
    # add value as tuple (value, position) into a list
    for line in f:
        if i>n:
            break
        if minPlayerScore == -1:
            minPlayerScore = int(line)
        elif minPlayerScore > int(line):
            minPlayerScore = int(line)
        avgPlayerScore += int(line)
        value.append((int(line), i))
        i += 1
    avgPlayerScore /= n 
    return n, k, value, avgPlayerScore, minPlayerScore

def initialize(list, k):
    listOpponent = []
    listSumScore = []
    for i in range(len(list)):
        j = 1
        sumOfOpponents = 0
        opponents = []
        half = k/2

        if k % 2 == 0:
            while j <= half:
                index = i+j
                if index > (len(list)-1):
                    index = index - len(list)
                sumOfOpponents += list[index][0]
                opponents.append(list[index])

                index = i-j
                if index < 0:
                    index = len(list) + index
                sumOfOpponents += list[index][0]
                opponents.append(list[index])

                j += 1

        else:
            # opposite node
            index = i+int(len(list)/2)
            if index > (len(list)-1):
                index = index - len(list)
            sumOfOpponents += list[index][0]
            opponents.append(list[index])

            while j <= half:
                # nearest next nodes
                index = i+j
                if index > (len(list)-1):
                    index = index - len(list)
                sumOfOpponents += list[index][0]
                opponents.append(list[index])

                # nearest previous nodes
                index = i-j
                if index < 0:
                    index = len(list) + index
                sumOfOpponents += list[index][0]
                opponents.append(list[index])

                j += 1

        listOpponent.append(opponents)
        listSumScore.append(sumOfOpponents)

    return listOpponent, listSumScore


main('input.txt', 'output.txt')
