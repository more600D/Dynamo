class rectangle():
    
    def __init__(self, s1=1, s2=1):
        self.side1 = s1
        self.side2 = s2
    
    def square(self):
        return self.side1 * self.side2


rec1 = rectangle(2, 6)
rec2 = rectangle(s2=2)

print(rec1.square(), rec2.square())