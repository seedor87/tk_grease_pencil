class my_obj():

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)

class my_sup():

    def __init__(self):
        self.val = None

    def exe(self):
        lis = list()
        self.val = my_obj(3)
        lis.append(self.val)
        print lis
        self.val = my_obj(5)
        lis.append(self.val)
        print lis
        self.val = my_obj(7)
        lis.append(self.val)
        print lis

        lis.pop()
        print lis

        self.val=my_obj(9)
        lis.append(self.val)
        print lis

        lis.pop()
        lis.pop()
        lis.pop()
        print lis

        try:
            lis.pop()
        except IndexError:
            pass

m = my_sup()
m.exe()