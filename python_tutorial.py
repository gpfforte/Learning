def dict_merge_sum(d1, d2):
    d3 = {}
    for key1, value1 in d1.items():
        if key1 not in d3.keys():
            d3[key1] = value1
        for key2, value2 in d2.items():
            if key2 not in d3.keys():
                d3[key2] = value2
            if key1 == key2:
                d3[key2] = value1+value2
            # elif:
            #     d3[key2] = value2
    return d3


d1 = {"a": 1, "b": 2, "c": 4}
d2 = {"a": 1, "b": 2, "c": 4}

print(dict_merge_sum(d1, d2))
