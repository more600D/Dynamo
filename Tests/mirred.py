elems = UnwrapElement(IN[0])  # noqa

mirrored = []
for el in elems:
    if el.Mirrored:
        mirrored.append(el)

OUT = mirrored
