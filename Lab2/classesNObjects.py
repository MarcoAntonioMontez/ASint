class rpnCalculator:
    stack = []

    def pushValue (self,value):
        self.stack.append(value)


    def popValue (self):
        value = self.stack.pop()
        return value


    def add (self):
        value1 = self.popValue()
        value2 = self.popValue()
        sum = value1+value2
        self.pushValue(sum)

calculator = rpnCalculator();
calculator.pushValue(1)
calculator.pushValue(2)

calculator.add()
value=calculator.popValue()
print(value)

