import time, os

files = os.listdir(IN[2])
count = IN[1]
num = count
for i in range(10):
    if count + 1 < num:
        OUT = i
        count = IN[1]
