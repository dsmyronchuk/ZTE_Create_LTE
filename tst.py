def binary_array_to_number(arr):
    ln = len(arr)
    dct = {k: 2 ** (k-1) for k in range(ln, 0, -1)}
    print(dct)
    return sum([dct[ln-e] for e, i in enumerate(arr) if i == 1])


print(binary_array_to_number([0, 1, 1, 0]))
# binary_array_to_number([0, 0, 0, 1])
# binary_array_to_number([0, 0, 1, 0])
# binary_array_to_number([1, 1, 1, 1])
# binary_array_to_number([0, 1, 1, 0])
# Testing for arr = [1, 0]: 8 should equal 2

print(binary_array_to_number([1, 0, 0, 0]))