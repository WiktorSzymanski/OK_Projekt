import copy
import random


def greedy(processes, NumOfProcessors, NumOfProces):
    iterArr = [x for x in range(1, NumOfProces + 1, 1)]
    # print(iterArr)

    minTime = None
    minComb = []

    processors = []
    processorsTime = []
    for i in range(0, NumOfProcessors, 1):
        processors.append([])
        processorsTime.append(0)

    for i in iterArr:
        minimum = processorsTime[0]
        indexOfLowestTimeProcessor = 0
        idx = 0
        for j in processorsTime:
            if j < minimum:
                indexOfLowestTimeProcessor = idx
                minimum = j
            idx += 1

        processors[indexOfLowestTimeProcessor].append(processes[i - 1])
        processorsTime[indexOfLowestTimeProcessor] += processes[i - 1]

    if None == minTime or max(processorsTime) < minTime:
        minTime = max(processorsTime)
        minComb = copy.deepcopy(processors)

    return minComb


def move(p, tabu_min, tabu_max):
    min=sum(p[0])
    min_idx = 0
    max = sum(p[0])
    max_idx = 0
    for i in range(1,len(p)):
        if sum(p[i]) < min and i not in tabu_min :
            min = sum(p[i])
            min_idx = i
        if sum(p[i])>max and i not in tabu_max:
            max = sum(p[i])
            max_idx = i


    dif = max - min
    min_to_dif = p[max_idx][0]
    min_to_dif_idx = 0
    for i in range(1, len(p[max_idx])):
        if abs(p[max_idx][i]-dif/2)<min_to_dif:
            min_to_dif =p[max_idx][i]
            min_to_dif_idx = i
    p[min_idx].append(min_to_dif)
    del p[max_idx][min_to_dif_idx]
    return p,min_idx,max_idx

def processing_time(p):
    max_proc = sum(p[0])
    for i in p:
        max_proc = max(sum(i), max_proc)
    return max_proc

def TabuSearch(proc, NumOfProcessors, NumOfProces):
    l = 4
    # int(input("Podaj oczekiwana dlugosc listy tabu"))
    n = 2
    # int(input("Podaj liczbe innych rozwiazan do sprawdzenia"))
    Best = proc
    print (*proc)
    tabu_list_min = []
    tabu_list_max = []
    neightbourhood = []
    while True:
        while len(neightbourhood) < n:
            if len(tabu_list_min) > l and len(tabu_list_max) >l:
                tabu_list_min.pop()
                tabu_list_max.pop()
            proc, min, max = move(Best,tabu_list_min, tabu_list_max)
            neightbourhood.append(proc)
            tabu_list_min.append(min)
            tabu_list_max.append(max)
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
    for i in ["m50.txt"]:
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
