elems = UnwrapElement(IN[0])

mirrored = []
for el in elems:
    if el.Mirrored:
        mirrored.append(el)

OUT = mirrored