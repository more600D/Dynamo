more_list = IN[0]  # noqa
less_list = IN[1]  # noqa
ll = []

# for l in range(len(el_list)):
# 	i = el_list.index(min(el_list))
# 	min_list.append(el_list[i])
# 	del el_list[i]


def notNone(li):
    f_list = []
    for i in li:
        sp = []
        for j in i:
            if j:
                sp.append(j)
        f_list.append(sp)
    return f_list

for i in range(len(more_list)):
    min_list = []
    part = []
    val = []
    ind = []
    if len(less_list) > 0:
        for j in range(len(less_list)):
            if more_list[i] + less_list[j] <= 10:
                val.append(less_list[j])
                ind.append(j)
            inx = val.index(max(val))
        del less_list[ind[inx]]
        min_list.append(max(val))
        min_list.append(more_list[i])
    else:
        min_list.append(more_list[i])
    ll.append(min_list)

OUT = ll
