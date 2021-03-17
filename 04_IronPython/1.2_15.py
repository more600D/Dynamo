bprint(selection)


def get_sum_id(items):
    result = 0
    for i in items:
        result += i.Id.IntegerValue
    print(result)


get_sum_id(selection)
