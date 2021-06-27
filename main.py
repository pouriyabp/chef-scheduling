class Food:
    def __init__(self, name, cook_time, deliver, period):
        self.name = name
        self.cookTime = int(cook_time)
        self.deliver = int(deliver)
        self.period = int(period)

    def __repr__(self):
        return f"{self.name} cook in {self.cookTime}, must deliver in {self.deliver}, come every {self.period}"


food1 = Food("Food1", 2, 2, 8)
food2 = Food("Food2", 1, 3, 4)
food3 = Food("Food3", 3, 6, 8)

print(food1)
print(food2)
print(food3)
