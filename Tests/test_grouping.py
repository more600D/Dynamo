import random
import itertools


class Element():
    def __init__(self, level, width):
        self.Level = level
        self.Width = width

    def __str__(self):
        return "{}, {}".format(self.Level, self.Width)


elements = []
for i in range(50):
    elements.append(Element(random.randint(0, 5), random.randrange(100, 500, 100)))

groups_by_level = itertools.groupby(
    sorted(elements, key=lambda x: x.Level),
    key=lambda x: x.Level
)

for key, group in groups_by_level:
    groups_by_width = itertools.groupby(
        sorted(group, key=lambda x: x.Width),
        key=lambda x: x.Width
    )

    for key, subgroup in groups_by_width:
        for el in subgroup:
            print(el)
        print
    print
