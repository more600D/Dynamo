
a = [3, 5, -8, 78, 0]


def bubble(mylist):
    last_item = len(mylist) - 1  # Сортировка пузырьков
    for i in range(0, last_item):
        for j in range(0, last_item - i):
            if mylist[j] < mylist[j + 1]:
                mylist[j], mylist[j + 1] = mylist[j + 1], mylist[j]
    return mylist


# def GreedyAlgo(dl, klv, sm):
#     aArr = []
#     bArr = []
#     k = 0
#     if isinstance(dl, list):
#         for i in range(len(dl)):
#             if dl[i] > 0:
#                 k += 1
#                 aArr.append(dl[i])
#     bubble(aArr)
#     b = 0
#     bFlag = True
#     while bFlag:
#         bFlag = False
#         b += 1
#         for i in range(k):
#             if sm >= aArr[i] and not bArr[i]:
#                 sm -= aArr[i]
#                 bArr.append(True)
#                 bFlag = True

elem = IN[0]  # noqa
elem = bubble(elem)
lengh_part = 1100
all_parts = []
for i in range(len(elem)):
    part = []
    part.append(elem[i])
    p_max = []
    for j in range(len(elem)):
        if elem[i] + elem[j] < lengh_part:
            p_max.append(elem[j])
    if len(p_max) > 0:
        part.append(p_max)
    all_parts.append(part)

OUT = all_parts, bubble(elem)
