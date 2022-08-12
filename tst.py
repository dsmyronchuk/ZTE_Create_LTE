lst = [15, 16, 17]

if len(lst) < 32:
    for j in range(32 - len(lst)):
        lst.append('65355')

print(lst)
print(len(lst))

