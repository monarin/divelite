class Car:
    wheels=0
    def __init__(self, n_wheels):
        self.wheels = n_wheels
    def run(self):
        print(f"I'm a car with {self.wheels} wheels")

class Truck(Car):
    def run(self):
        print(f"I'm a truck with {self.wheels} wheels")
        super().run()
    #pass


c = Car(4)
c.run()
v = Truck(6)
v.run()
