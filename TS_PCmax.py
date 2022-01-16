import copy
from timeit import default_timer as timer

TIME_LIMIT_PER_FILE = 300
# in seconds

class Processor():
  def __init__(self,processes, time = 0):
    self.processes = processes
    self.time = time
  def calculateTime(self):
    newTime = 0
    for process in self.processes:
      newTime += process

    self.time = newTime

def greedy(processes, numOfProcessors):
  processors = []

  for _ in range(0, numOfProcessors, 1):
    processors.append(Processor([]))


  for proces in processes:
    minimumProcessor = processors[0]
    indexOfLowestTimeProcessor = 0
    i = 0

    for processor in processors:
      if processor.time < minimumProcessor.time:
        indexOfLowestTimeProcessor = i
        minimumProcessor = processors[i]
      i += 1

    processors[indexOfLowestTimeProcessor].processes.append(proces)
    processors[indexOfLowestTimeProcessor].calculateTime()

  return processors

def bestSwap(processorsTable, indexOfMinTimeProcessor, indexOfMaxTimeProcessor, diffToLookFor):
  for idMax,processMax in enumerate(processorsTable[indexOfMaxTimeProcessor].processes):
    for idMin,processMin in enumerate(processorsTable[indexOfMinTimeProcessor].processes):
      if processMax - processMin == diffToLookFor:
        return True, idMax, idMin
  
  return False, None, None

def findBestMove(processorsTable,swichController):
  # switchController decides how many moves we need to reject before the one we can use

  indexOfMinTimeProcessor = None
  indexOfMaxTimeProcessor = None

  # print("I'm in findBestMove")

  rejectTable = []
  # rejectTable is table with max and min combinations we can't use !!! if TabuList is to big we may need to modify it !!!

  for _ in range(swichController):
    rejectTable.append(indexOfMinTimeProcessor)
    for i in range(len(processorsTable)):
      # print("I'm in for")
      if (indexOfMinTimeProcessor == None or processorsTable[indexOfMinTimeProcessor].time > processorsTable[i].time) and i not in rejectTable:
        indexOfMinTimeProcessor = i

    
      if (indexOfMaxTimeProcessor == None or processorsTable[indexOfMaxTimeProcessor].time < processorsTable[i].time) and i not in rejectTable:
        indexOfMaxTimeProcessor = i

  # print("I'm out of for")

  differenceBetweenMinAndMaxTimes = processorsTable[indexOfMaxTimeProcessor].time - processorsTable[indexOfMinTimeProcessor].time

  # print("differenceBetweenMinAndMaxTimes is ", differenceBetweenMinAndMaxTimes)
  # print("Minimalny czas w findBestMove ",minTimeToFinish(processorsTable))
  # i = input("Press Enter to continue (You are in findBestMove): ")

  foundProcessToSwitch = False
  differenceToMostOptimal = 0

  while(not foundProcessToSwitch):
    # print("doin while")
    for i,process in enumerate(processorsTable[indexOfMaxTimeProcessor].processes):
      # print("I'm in for with enumerate")
      if process == differenceBetweenMinAndMaxTimes//2 + differenceToMostOptimal or process == differenceBetweenMinAndMaxTimes//2 - differenceToMostOptimal:
        transfer = processorsTable[indexOfMaxTimeProcessor].processes.pop(i)
        # print("Transfer ", transfer)
        processorsTable[indexOfMinTimeProcessor].processes.append(transfer)

        processorsTable[indexOfMaxTimeProcessor].calculateTime()
        processorsTable[indexOfMinTimeProcessor].calculateTime()

        # print("Returning from findBestMove")
        return processorsTable

      BSDiffPlus, BSDiffPlusIdMax, BSDiffPlusIdMin = bestSwap(processorsTable, indexOfMinTimeProcessor, indexOfMaxTimeProcessor, differenceBetweenMinAndMaxTimes//2 + differenceToMostOptimal)

      if BSDiffPlus:
        transferMin = processorsTable[indexOfMinTimeProcessor].processes.pop(BSDiffPlusIdMin)
        transferMax = processorsTable[indexOfMaxTimeProcessor].processes.pop(BSDiffPlusIdMax)

        processorsTable[indexOfMinTimeProcessor].processes.append(transferMax)
        processorsTable[indexOfMaxTimeProcessor].processes.append(transferMin)

        processorsTable[indexOfMaxTimeProcessor].calculateTime()
        processorsTable[indexOfMinTimeProcessor].calculateTime()

        # print("Returning from findBestMove")
        return processorsTable

      else:
        BSDiffMinus, BSDiffMinusMax, BSDiffMinusMin = bestSwap(processorsTable, indexOfMinTimeProcessor, indexOfMaxTimeProcessor, differenceBetweenMinAndMaxTimes//2 - differenceToMostOptimal)

        if BSDiffMinus:
          transferMin = processorsTable[indexOfMinTimeProcessor].processes.pop(BSDiffMinusMin)
          transferMax = processorsTable[indexOfMaxTimeProcessor].processes.pop(BSDiffMinusMax)

          processorsTable[indexOfMinTimeProcessor].processes.append(transferMax)
          processorsTable[indexOfMaxTimeProcessor].processes.append(transferMin)

          processorsTable[indexOfMaxTimeProcessor].calculateTime()
          processorsTable[indexOfMinTimeProcessor].calculateTime()

          # print("Returning from findBestMove")
          return processorsTable
    
    differenceToMostOptimal += 1

def move(processorsTable, tabuList, l, startTime):

  # print("I'm in the move")

  switchController = 1

  bestMove = findBestMove(copy.deepcopy(processorsTable),switchController)

  notInTabuList = True

  for list in tabuList:
    if compareProcessorsTab(list,bestMove):
      notInTabuList = False
      break

  while(not notInTabuList and (timer() - startTime) < TIME_LIMIT_PER_FILE):
    print("Doin move that is not in tabu list")
    switchController += 1
    bestMove = findBestMove(copy.deepcopy(bestMove),switchController)

    for list in tabuList:
      if not compareProcessorsTab(list,bestMove):
        notInTabuList = True


  if len(tabuList) >= l:
    tabuList.pop(0)
  
  tabuList.append(copy.deepcopy(bestMove))
  

  # print("Returning best move")

  return bestMove

def minTimeToFinish(processorsTable):
  minTime = None
  for process in processorsTable:
    if minTime == None or minTime < process.time:
      minTime = process.time
  
  return minTime

def TabuSearch(processorsTable):
  startTime = timer()
  # max tabu list length
  l = 1
  # max neightbourhood length
  n = 1
  currentBestCombination = copy.deepcopy(processorsTable)
  allTimeBest = copy.deepcopy(processorsTable)
  sameBestResoultCounter = 0
  tabuList = []

  while (timer() - startTime) < TIME_LIMIT_PER_FILE:

    # print("Creating neightbourhood")

    # print("Entering with min time :", minTimeToFinish(currentBestCombination))
    # i = input("Press Enter to continue: ")

    neightbourhood = []

    while len(neightbourhood) < n:

      # print("Doin the move")

      processorsTable = move(copy.deepcopy(currentBestCombination),tabuList,l,startTime)

      # print("Created one")
      # print("Min time of hood component :", minTimeToFinish(processorsTable))
      # i = input("Press Enter to continue: ")

      neightbourhood.append(processorsTable)

    minTimesFromHood = []
    timeOfBestCombination = None

    for id,hood in enumerate(neightbourhood):
      minTimesFromHood.append(minTimeToFinish(hood))

      # print("Hood nr ",id)
      # for i in range(len(hood)):
      #   print(*hood[i].processes)
      #   print("Time: ",hood[i].time)
      #   print()
      # print()
    
    for i,time in enumerate(minTimesFromHood):
      if timeOfBestCombination == None or timeOfBestCombination > time:
        timeOfBestCombination = time
        currentBestCombination = copy.deepcopy(neightbourhood[i])

    if (minTimeToFinish(allTimeBest) > timeOfBestCombination):
      allTimeBest = copy.deepcopy(currentBestCombination)
      sameBestResoultCounter = 0
    else:
      sameBestResoultCounter += 1

    if (sameBestResoultCounter >= 100):
      break
    


    # print("Altualny minimalny czas: " + str(timeOfBestCombination))

    # for i in range(len(allTimeBest)):
    #   print(*allTimeBest[i].processes)
    #   print("Time: ",allTimeBest[i].time)
    #   print()
    # print()

    print("Ogolny minimalny czas: " + str(minTimeToFinish(allTimeBest)))

    # i = input("Press Enter to continue, 1 to stop while: ")
    # if i == "":
    #   i = 0
      
    # if int(i) == 1:
    #   return
  
  return minTimeToFinish(allTimeBest),allTimeBest
  

def compareProcessorsTab(processorsTab1,processorsTab2):
  if len(processorsTab1) != len(processorsTab2):
    return False
  
  for i in range(len(processorsTab1)):
    if processorsTab1[i].processes != processorsTab2[i].processes:
      return False

  return True

def main():
      
  # for i in range(2):
  #   processors = 10 * (i + 1)
  #   for i in range(10):
  #     numOfProcesses = 100 * (i + 1)
  #     name = "test_p" + str(processors) + "_" + str(numOfProcesses) + ".txt"
      resultsTab = []
      filesTab = ["m25.txt" , "m50.txt", "m50n1000.txt", "m50n200.txt", "m10n200.txt"]
      for nameOfFile in filesTab:
        singleResult = []
        # "m25.txt" , "m50.txt", "m50n1000.txt", "m50n200.txt", "m10n200.txt"]:
        with open(nameOfFile, "r") as file:
          numOfProcessors = int(file.readline())
          numOfProces = int(file.readline())
          processes = []
          for nameOfFile in range(0, numOfProces, 1):
            processes.append(int(file.readline()))

        # print("Data Imported")

        entryProcessorsTable = greedy(processes, numOfProcessors)

        # for i in range(numOfProcessors):
          # print(*entryProcessorsTable[i].processes)
          # print("Time: ",entryProcessorsTable[i].time)

        print("Greedy Algorythm Done")
        print("Time: " + str(minTimeToFinish(entryProcessorsTable)))

        # print(findBestMove(entryProcessorsTable))

        print("Tabu")
        time,tab = TabuSearch(entryProcessorsTable)
        singleResult.append(time)
        singleResult.append(tab)
        resultsTab.append(singleResult)
      print("Wyniki:")

      for i,name in enumerate(filesTab):
        print(name + "\t\ttime: " + str(resultsTab[i][0]))

      i = input("Press Enter to end, 1 to print results combinations: ")
      if i == "":
        i = 0
        
      if int(i) == 1:
        for i,name in enumerate(filesTab):
          print(name + " result:\n")
          for j in range(len(resultsTab[i][1])):
            print("\tP" + str(j+1) +":\t",*resultsTab[i][1][j].processes)

            print()
      


main()
# Krok -> mieszanie między procesorami zadań
# Ruch -> Zmiana najdluzszego zdania procesora
# najdluzej pracującego na zadanie najdluzsze w najmniej obciazonym
# Ruch -> wstawianie do procora najkrotszego polowy wartosci
# roznicy czasu wykonania zadaan miedzy min i max