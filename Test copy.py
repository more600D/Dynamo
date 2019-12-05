
a = [3, 5, -8, 78, 0]


def bubble(mylist):
    last_item = len(mylist) - 1  # Сортировка пузырьков
    for i in range(0, last_item):
        for j in range(0, last_item - i):
            if mylist[j] > mylist[j + 1]:
                mylist[j], mylist[j + 1] = mylist[j + 1], mylist[j]
    return mylist

# def GreedyAlgo(dl, klv, sm, optinal_shrez = 0, optional_krm = 0):
#     aArr = []
#     bArr = []
#     bFlag = False
#     k = 0
#     if isinstance(dl, list):
#         for i in range(len(dl)):
#             if dl[i] > 0:
#                 k += 1
#                 aArr.append(dl[i])
#     bubble(aArr)


print(bubble(a))
