data = IN[0]
name = IN[1]

info = []
for key in data.keys():
    if key in name:
        value, id = data[key], key
        d = "DONE"
        break
    else:
        d = "UNDONE"
info.append("{}:{} - {}".format(id, value, d))

OUT = info
