def config_selection(obj):

    first_elem = list(obj)[0]  # '1,4' // '1'  формат который получается
    if len(obj) == 2 and len(first_elem) == 3:
        return '2x2'

    elif len(obj) == 2 and len(first_elem) == 1:
        return '2x1'

    elif len(obj) == 1 and len(first_elem) == 3:
        return '1x2'

    elif len(obj) == 1 and len(first_elem) == 1:
        return '1x1'


a = [{'51': '1,4'}]
print(config_selection(a))