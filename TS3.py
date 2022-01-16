import copy


def greedy(processes, NumOfProcessors, NumOfProces):
    minTime = None
    minComb = []

    processors = []

    for i in range(0, NumOfProcessors, 1):
        processors.append([[],0])


    for proces in processes:
        minimum = processors[0][1]
        indexOfLowestTimeProcessor = 0
        idx = 0
        for processor in processors:
            if processor[1] < minimum:
                indexOfLowestTimeProcessor = idx
                minimum = processor[1]
            idx += 1

        processors[indexOfLowestTimeProcessor][0].append(proces)
        processors[indexOfLowestTimeProcessor][1] += proces

    newMinTime = 0
    for processor in processors:
          if newMinTime < processor[1]:
            newMinTime = processor[1]

    if None == minTime or newMinTime < minTime :
        minTime = newMinTime
        minComb = copy.deepcopy(processors)
    
    return minComb

def move(p, tabuList, l):
    result = copy.deepcopy(p)
    indexOfMinTimeProcessor = None
    minTime = None
    indexOfMaxTimeProcessor = None
    maxTime = None

    for i in range(len(result)):
      if indexOfMinTimeProcessor == None or minTime > result[i][1]:
        indexOfMinTimeProcessor = i
        minTime = result[i][1]
      
      if indexOfMaxTimeProcessor == None or maxTime < result[i][1]:
        indexOfMaxTimeProcessor = i
        maxTime = result[i][1]
    
    differenceBetweenMinAndMaxTimes = maxTime = minTime

    for i in range(len(result[indexOfMaxTimeProcessor][0])):
      if result[indexOfMaxTimeProcessor][0][i] == differenceBetweenMinAndMaxTimes:
        process = result[indexOfMaxTimeProcessor][0].pop(i)

        result[indexOfMaxTimeProcessor][1] -= process
        result[indexOfMinTimeProcessor][0].append(process)
        result[indexOfMinTimeProcessor][1] += process

    while(result in tabuList):
      indexOfMinTimeProcessor = None
      minTime = None
      indexOfMaxTimeProcessor = None
      maxTime = None

      for i in range(len(result)):
        if indexOfMinTimeProcessor == None or minTime > result[i][1]:
          indexOfMinTimeProcessor = i
          minTime = result[i][1]
        
        if indexOfMaxTimeProcessor == None or maxTime < result[i][1]:
          indexOfMaxTimeProcessor = i
          maxTime = result[i][1]
      
      differenceBetweenMinAndMaxTimes = maxTime = minTime

      found = 0
      diff = 0
      while(found != 1):
        
        for i in range(len(result[indexOfMaxTimeProcessor][0])):
          if result[indexOfMaxTimeProcessor][0][i] == differenceBetweenMinAndMaxTimes + diff or result[indexOfMaxTimeProcessor][0][i] == differenceBetweenMinAndMaxTimes - diff:
            process = result[indexOfMaxTimeProcessor][0].pop(i)

            result[indexOfMaxTimeProcessor][1] -= process
            result[indexOfMinTimeProcessor][0].append(process)
            result[indexOfMinTimeProcessor][1] += process
            found = 1
            break
        
        diff += 1



    if tabuList == l:
      tabuList.pop(0)
      tabuList.append(result)
    else: 
      tabuList.append(result)

    return result


def processing_time(p):
    newMinTime = 0
    for processor in p:
      if newMinTime < processor[1]:
        newMinTime = processor[1]

    return newMinTime

def TabuSearch(proc, NumOfProcessors, NumOfProces):
    l = 4
    # int(input("Podaj oczekiwana dlugosc listy tabu"))
    n = 2
    # int(input("Podaj liczbe innych rozwiazan do sprawdzenia"))
    Best = proc
    print (*proc)
    neightbourhood = []
    tabuList = []
    while True:
        while len(neightbourhood) < n:
            proc = move(Best,tabuList,l)
            neightbourhood.append(proc)
        times =[]
        for x in neightbourhood:
             times.append(processing_time(x))
             min_time = times[0]

        for y in range(len(times)):
            if times[y] < min_time:
                min_time = times[y]
                Best = neightbourhood[y]
        print(*proc)

        print("Altualny minimalny czas: " + str(min_time))


def main():
    for i in ["m50n1000.txt"]:
        # m50.txt", "m50n1000.txt", "m50n200.txt", "m10n200.txt"]:
        with open(i, "r") as file:
            NumOfProcessors = int(file.readline())
            NumOfProces = int(file.readline())
            processes = []
            for i in range(0, NumOfProces, 1):
                processes.append(int(file.readline()))

        #rocesses.sort(reverse=True)
        proc = greedy(processes, NumOfProcessors, NumOfProces)

        TabuSearch(proc,NumOfProcessors, NumOfProces)


main()
# Krok -> mieszanie między procesorami zadań
# Ruch -> Zmiana najdluzszego zdania procesora
# najdluzej pracującego na zadanie najdluzsze w najmniej obciazonym
# Ruch -> wstawianie do procora najkrotszego polowy wartosci
# roznicy czasu wykonania zadaan miedzy min i max
