import random
import numpy as np

def ReadData () :
    f = open("p45")
    i = 0
    demandRowCount = 0
    global n
    global m
    global distance
    global capacity
    global fixed_c
    global d_garden
    fixed_c = []
    d_garden = []
    capacity = []
    n = 0
    m = 0
    r_well = 0
    try:
        for line in f:
            line = line.replace('\n', "")
            tmps = line.split(" ")
            tmp = []

            for item in tmps :
                if item != "":
                    tmp.append(item)

            if i == 0:

                n = int(tmp[0])
                m = int(tmp[1])
                r_well = n // 10
                demandRowCount = m // 10
            elif i <= n:

                capacity.append(int(tmp[0]))
                fixed_c.append(int(tmp[1]))
            elif i <= n + demandRowCount:
                tmp = line.replace(".", "")
                tmp = tmp.split(" ")
                for item in tmp:
                    if item != "":
                        d_garden.append(int(item))
            elif i <= n + demandRowCount + m * r_well :
                tmpNum = []
                tmp = line.replace(".", " ")
                tmp = tmp.split(" ")
                for item in tmp:
                    if item != "":
                        tmpNum.append(int(item))

                distance.append(tmpNum)
            i = i + 1
        if r_well != 1:
            for i in range (m):
                for j in range(1, r_well):
                    distance[i] = distance[i] + distance[i * r_well + j]

            distance = distance[0:m]
        f.close()
    except:
        print("file doesn't here")
        pass


def produce_randan_solution():
    well_open = [0] * n
    garden_assign = []
    total_fixed_c = 0
    total_cost = 0
    d_garden_copy = d_garden.copy()
    capacity_copy = capacity.copy()

    for i in range(m) :
        flag = True
        well_n = -1
        while (flag) :
            well_n = random.randint(0, n - 1)

            if (d_garden_copy[i] <= capacity_copy[well_n]) :

                if (well_open[well_n] == 0) :
                    well_open[well_n] = 1
                    total_fixed_c += fixed_c[well_n]
                garden_assign.append(well_n)
                capacity_copy[well_n] -= d_garden_copy[i]
                total_cost += distance[i][well_n]
                flag = False

    return total_fixed_c + total_cost, well_open, garden_assign, capacity_copy



def Simulate_Anneal() :
    T0 = 1000
    Tmin = 1
    eta = 0.95
    tmp = produce_randan_solution()

    bestCost = tmp[0]
    bestwellOpen = tmp[1]
    bestValueAssign = tmp[2]
    capacity_copy = capacity.copy()
    ReadData()
    t = T0

    while(t >= Tmin):

        for j in range(1000):

            tmp1 = produce_randan_solution()
            costDiffence = tmp1[0] - bestCost

            if tmp1[0] < bestCost or np.exp(-costDiffence/(t))>np.random.rand():

                bestCost = tmp1[0]
                bestwellOpen = tmp1[1]
                bestValueAssign = tmp1[2]
                capacity_copy = tmp1[3]
        t = eta*t
    return bestCost, bestwellOpen, bestValueAssign


def Simulate_Anneal_test() :
        global n
        global m
        global distance
        global capacity
        global fixed_c
        global d_garden
        n = 0
        m = 0
        capacity = []
        fixed_c = []
        d_garden = []
        distance = []
        ReadData()
        tmp = Simulate_Anneal()
        print("Best costs")
        print(tmp[0])
        print("opened wellls")
        print(tmp[1])
        print("assigned wells for gardens")
        print(tmp[2])

if __name__ == '__main__':
    Simulate_Anneal_test()

