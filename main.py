from operator import attrgetter


class Food:
    def __init__(self, name, cook_time, deadline, period):
        self.name = name
        self.cookTime = int(cook_time)
        self.deadline = int(deadline)
        self.period = int(period)
        self.tempDeadline = int(deadline)
        self.tempCook = int(cook_time)

    def __repr__(self):
        return f"{self.name} tempdeadline={self.tempDeadline}"


def lcm(x, y):
    if x > y:
        greater = x
    else:
        greater = y
    while (True):
        if (greater % x == 0) and (greater % y == 0):
            lcm = greater
            break
        greater += 1
    return lcm


def calculate_chef_time(list_of_food):
    """
    calculate the LCM between foods
    :param list_of_food: list of foods
    :return: LCM between foods period
    """
    time = 1
    for food in list_of_food:
        time = lcm(food.period, time)
    return time


def check_do_order(list_of_food, chef_time):
    """
    check that chef can do this order or not
    :param list_of_food: list of foods
    :param chef_time: the time that chef spend in kitchen(use calculate chef time function to calculate this param)
    :return: if chef can do this job return true else return false
    """
    result = 0
    for food in list_of_food:
        count = food.period / chef_time
        result += food.cookTime * count
    if result <= chef_time:
        return True
    else:
        return False


def earliest_deadline_first(list_of_foods, chef_time):
    i = 0
    idle_time = 0
    temp_list = list_of_foods.copy()
    while i < chef_time:
        if len(temp_list) == 0:
            print(f"{i} Idle.")
            idle_time += 1
            i += 1
            for food in list_of_foods:
                if i % food.period == 0:
                    # print(f"{i} {food.name} come.")
                    temp_list.append(food)
            continue
        # find minimum deadline between foods
        min_food = min(temp_list, key=attrgetter('tempDeadline'))
        # cook that food with minimum deadline
        print(f"{i} {min_food.name}.")
        min_food.tempCook -= 1
        # remove food if it's done
        if min_food.tempCook == 0:
            min_food.tempDeadline = min_food.deadline
            min_food.tempCook = min_food.cookTime
            temp_list.remove(min_food)

        i += 1
        for food in list_of_foods:
            if i % food.period == 0:
                # print(f"{i} {food.name} come.")
                temp_list.append(food)
        # like ageing increase priority each round with -1 deadline
        for food in temp_list:
            food.tempDeadline -= 1
            if food.tempDeadline == -1:
                print(f"{i} {food.name} miss the deadline.")
    print(f"idle time = {idle_time}")


food1 = Food("Food1", 2, 2, 8)
food2 = Food("Food2", 1, 3, 4)
food3 = Food("Food3", 3, 6, 8)

# list for store foods
arr_of_foods = [food1, food2, food3]
# chef time that spend in kitchen
chef_time_spend = calculate_chef_time(arr_of_foods)
for food in arr_of_foods:
    print(f"{food.name} cook in {food.cookTime}, deadline each period is {food.deadline}, come every {food.period}")

if check_do_order(arr_of_foods, chef_time_spend) is False:
    print("Can't handle orders!")
    exit()

print(f"the chef must be in kitchen for {chef_time_spend} period")
print(f"chef can do this order? {check_do_order(arr_of_foods, chef_time_spend)}")
earliest_deadline_first(arr_of_foods, chef_time_spend)
