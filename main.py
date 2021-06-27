class Food:
    def __init__(self, name, cook_time, deadline, period):
        self.name = name
        self.cookTime = int(cook_time)
        self.deadline = int(deadline)
        self.period = int(period)

    def __repr__(self):
        return f"{self.name} cook in {self.cookTime}, deadline each period is {self.deadline}, come every {self.period}"


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
    list of foods:param list_of_food:
    LCM between foods period:return:
    """
    time = 1
    for food in list_of_food:
        time = lcm(food.period, time)
    return time


def check_do_order(list_of_food, chef_time):
    """
    check that chef can do this order or not
    list of foods:param list_of_food:
    the time that chef spend in kitchen(use calculate chef time function to calculate this param):param chef_time:
    if chef can do this job return true else return false:return:
    """
    result = 0
    for food in list_of_food:
        count = food.period / chef_time
        result += food.cookTime * count
    if result <= chef_time:
        return True
    else:
        return False


food1 = Food("Food1", 2, 2, 8)
food2 = Food("Food2", 1, 3, 4)
food3 = Food("Food3", 3, 6, 8)

# list for store foods
arr_of_foods = [food1, food2, food3]
# chef time that spend in kitchen
chef_time = calculate_chef_time(arr_of_foods)
for food in arr_of_foods:
    print(food)

if check_do_order(arr_of_foods, chef_time) is False:
    print("Can't handle orders!")
    exit()


print(f"the chef must be in kitchen for {chef_time} period")
print(f"chef can do this order? {check_do_order(arr_of_foods, chef_time)}")
