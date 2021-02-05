data = {')': 1,
        '(': 1,
        '{': 2,
        '}': 2,
        '[': 3,
        ']': 3}

mylist = ['(', '{', '[', ']', '}', ')']

if len(mylist) % 2 == 0:
    if data[mylist[0]] == data[mylist[-1]]:
        print('balance')
else:
    print('no balance')
