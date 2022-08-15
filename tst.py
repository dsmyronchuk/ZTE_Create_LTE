a = 'aba'

def is_isogram(string):
    for i in string:
        if string.count(i) > 1:
            return False
    else:
        return True

print(is_isogram(a))