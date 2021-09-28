elems = UnwrapElement(IN[1])  # noqa

loc_point = []

for el in elems:
    if el.Location:
        loc_point.append(el.Location.Point)

OUT = loc_point
