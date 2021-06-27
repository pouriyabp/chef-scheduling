class Food:
    def __init__(self, name, cook_time, deliver, period):
        self.name = name
        self.cookTime = int(cook_time)
        self.deliver = int(deliver)
        self.period = int(period)

    def __repr__(self):
        return f"{self.name} cook in {self.cookTime}, must deliver in {self.deliver}, come every {self.period}"


def lcm(x, y):
    if x > y:
        greater = x
    else:
        greater = y
    while (True):
        if ((greater % x == 0) and (greater % y == 0)):
            lcm = greater
            break
        greater += 1
    return lcm


def calculate_chef_time(list_of_food):
    """
    calculate the LCM between foods
    input ---> list of foods
    output ---> LCM between foods period
    """
    time = 1
    for food in list_of_food:
        time = lcm(food.period, time)
    return time


food1 = Food("Food1", 2, 2, 8)
food2 = Food("Food2", 1, 3, 4)
food3 = Food("Food3", 3, 6, 8)

# list for store foods
arr_of_foods = [food1, food2, food3]

for food in arr_of_foods:
    print(food)

print(f"the chef must be in kitchen for {calculate_chef_time(arr_of_foods)} period")
