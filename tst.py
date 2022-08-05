from jinja2 import Template


class TST:
    lst_tst = []

    def __init__(self, lst_inp):
        self.one = lst_inp[0]
        self.two = lst_inp[1]
        self.three = lst_inp[2]

        self.__class__.lst_tst.append(self)


my_obj = TST([15, 16, 17])

temp = Template(open('template/txt_temp.txt').read()).render(obj=TST.lst_tst[0])
print(temp)