import copy

def test(table):
    table.append(1)
    return table


tab = [1,2,3]

tab2 = tab

for i in range(1):
    print("YOoo")

tab2.append(1)
tab.append(5)
print(test(copy.deepcopy(tab)))
print(tab2)
print(97//2)