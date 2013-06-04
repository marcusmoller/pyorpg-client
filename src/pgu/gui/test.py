
class Test(object):

    @property
    def something(self):
        return 12

    @something.setter
    def something(self, value):
        self.other = value

t = Test()

print t.something

t.something = 123
print t.other

