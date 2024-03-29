from operator import attrgetter


class Food:
    def __init__(self, name, cook_time, deadline, period):
        self.name = name
        self.cookTime = int(cook_time)  # original data that user input
        self.deadline = int(deadline)  # original data that user input
        self.period = int(period)  # original data that user input
        self.tempDeadline = int(deadline)  # change this without original data changed
        self.tempCook = int(cook_time)  # change this without original data changed
        self.missFood = int(deadline)  # for check deadline is missed or not
        self.waitingTime = 0  # use this for calculate waiting time
        self.lastEnter = 0  # use this (and tempCook) for calculate change between foods
        self.priority = 0  # set food priority
        self.predict = False  # for predict deadline ---> if true means we predict for this food

    def __repr__(self):
        return f"{self.name}"

    # initializer (for each scheduling function we should use this)
    def set_value(self):
        """
        set initial value like __init__
        use this function at start of each scheduling algorithm.
        :return: nothing return ---> only set value to class attributes
        """
        self.predict = False
        self.priority = 0
        self.lastEnter = 0
        self.waitingTime = 0
        self.missFood = int(self.deadline)
        self.tempCook = int(self.cookTime)
        self.tempDeadline = int(self.deadline)

    def set_priority_for_llf(self):
        """
        set priority for least laxity first
        :return: nothing return ---> set priority of each food
        """
        self.priority = self.tempDeadline - self.tempCook

    def set_priority_for_edf(self):
        """
        set priority for earliest deadline first
        :return: nothing return ---> set priority of each food
        """
        self.priority = self.tempDeadline

    def set_priority_for_rate_monotonic(self):
        """
        set priority for rate monotonic
        :return: nothing return ---> set priority of each food
        """
        self.priority = self.period


def lcm(x, y):
    """
    calculate the LCM between 2 number
    :param x: first number
    :param y: second number
    :return: the LCM between x and y
    """
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
        count = chef_time / food.period
        result += food.cookTime * count
    if result <= chef_time:
        return True
    else:
        return False


def predict_miss_deadline(list_temp_foods, round):
    """
    this function predict the food that miss the deadline.
    first we calculate how many food have better priority than the food we choose.
    then we use that number and tempDeadline for that food and compare it with tempCook.
    with this compare we can understand that our food will miss the deadline or not.
    :param list_temp_foods: list of foods that are in come and wait for cooked.
    :param round: the round that we try to predict for find the miss food.
    :return: nothing return ---> print in terminal.
    """
    for food in list_temp_foods:
        food_with_better_priority = 0
        for otherfood in list_temp_foods:
            if otherfood == food:
                continue
            elif otherfood.priority < food.priority:
                food_with_better_priority += 1
            else:
                continue
        if food.tempDeadline - food_with_better_priority < food.tempCook and food.predict is False:
            print(f"{round} {food.name} will miss the deadline.")
            food.predict = True


def least_laxity_first(list_of_foods, chef_time):
    """
    least laxity first scheduling algorithm.
    this algorithm priority is tempDeadline - tempCook that use set_priority_for_llf function in Food class.
    in first check if list is empty the chef is idle and increase round and check new foods must come in new round.
    next get food with minimum priority and decrease tempCook and if tempCook is 0 that means the food is done so
    remove the food from list.
    each round decrease tempDeadline and miss food for find use them in predict miss food and find miss food.
    save food in last_food to find changes between foods if last_food is changed and tempCook is not equal to original
    cook time.
    at the end calculate the new foods that must come in new round.
    :param list_of_foods: list of food that chef must cook.
    :param chef_time: maximum time that chef in kitchen.
    :return: nothing return ---> print in terminal
    """
    print(60 * "*")
    print("Least laxity first")
    # set value
    for food in list_of_foods:
        food.set_value()
    i = 0
    idle_time = 0
    change_between_foods = 0
    temp_list = list_of_foods.copy()
    last_food = None
    while i < chef_time:
        # check if list is empty print idle and add new foods
        if len(temp_list) == 0:
            print(f"{i} Idle.")
            idle_time += 1
            i += 1
            for food in list_of_foods:
                if i % food.period == 0:
                    # print(f"{i} {food.name} come.")
                    temp_list.append(food)
            continue
        for food in list_of_foods:
            food.set_priority_for_llf()
        # find food with minimum priority
        min_food = min(temp_list, key=attrgetter('priority'))
        # calculate change food
        if i == 0:
            pass
        elif min_food != last_food and last_food.tempCook != last_food.cookTime:
            print(f"Chef change food in round {i}")
            change_between_foods += 1
        # cook that food with minimum priority
        print(f"{i} {min_food.name}.")
        min_food.tempCook -= 1
        # remove food if it's done
        if min_food.tempCook == 0:
            min_food.predict = False
            min_food.priority = 0
            min_food.tempDeadline = min_food.deadline
            min_food.tempCook = min_food.cookTime
            min_food.missFood = min_food.deadline
            min_food.waitingTime += ((i + 1) - min_food.lastEnter) - min_food.cookTime
            temp_list.remove(min_food)
        for food in temp_list:
            # use this for predict miss deadline food
            food.tempDeadline -= 1
            food.missFood -= 1
            if food.missFood == 0:
                print(f"{i} {food.name} miss the deadline.")
            # set min_food as last_food that we use in calculate change between foods
        last_food = min_food
        # predict miss foods
        predict_miss_deadline(temp_list, i)
        i += 1
        # add food that must come every period
        for food in list_of_foods:
            if i % food.period == 0:
                # print(f"{i} {food.name} come.")
                food.lastEnter = i
                # print(f"{food.name} enter {food.lastEnter}")
                temp_list.append(food)

    print(f"idle time = {idle_time}.")
    for food in list_of_foods:
        print(f"{food.name} waiting time = {food.waitingTime}.")
    print(f"change between foods is {change_between_foods}.")


def rate_monotonic(list_of_foods, chef_time):
    """
    rate monotonic scheduling algorithm.
    this algorithm priority is minimum period between foods.
    in first check if list is empty the chef is idle and increase round and check new foods must come in new round.
    next get food with minimum period and decrease tempCook and if tempCook is 0 that means the food is done so
    remove the food from list.
    each round decrease tempDeadline and miss food for find use them in predict miss food and find miss food.
    save food in last_food to find changes between foods if last_food is changed and tempCook is not equal to original
    cook time.
    at the end calculate the new foods that must come in new round.
    :param list_of_foods: list of food that chef must cook.
    :param chef_time: maximum time that chef in kitchen.
    :return: nothing return ---> print in terminal
    """
    print(60 * "*")
    print("Rate monotonic")
    # set value
    for food in list_of_foods:
        food.set_value()
    i = 0
    idle_time = 0
    change_between_foods = 0
    temp_list = list_of_foods.copy()
    last_food = None
    while i < chef_time:
        # check if list is empty print idle and add new foods
        if len(temp_list) == 0:
            print(f"{i} Idle.")
            idle_time += 1
            i += 1
            for food in list_of_foods:
                if i % food.period == 0:
                    # print(f"{i} {food.name} come.")
                    temp_list.append(food)
            continue
        for food in list_of_foods:
            food.set_priority_for_rate_monotonic()
        # find minimum period between foods
        min_food = min(temp_list, key=attrgetter('period'))
        # calculate change food
        if i == 0:
            pass
        elif min_food != last_food and last_food.tempCook != last_food.cookTime:
            print(f"Chef change food in round {i}")
            change_between_foods += 1
        # cook that food with minimum period
        print(f"{i} {min_food.name}.")
        min_food.tempCook -= 1
        # remove food if it's done
        if min_food.tempCook == 0:
            min_food.predict = False
            min_food.priority = 0
            min_food.tempDeadline = min_food.deadline
            min_food.tempCook = min_food.cookTime
            min_food.missFood = min_food.deadline
            min_food.waitingTime += ((i + 1) - min_food.lastEnter) - min_food.cookTime
            temp_list.remove(min_food)
        for food in temp_list:
            # use this for predict miss deadline food
            food.tempDeadline -= 1
            food.missFood -= 1
            if food.missFood == 0:
                print(f"{i} {food.name} miss the deadline.")
        # set min_food as last_food that we use in calculate change between foods
        last_food = min_food
        # predict miss foods
        predict_miss_deadline(temp_list, i)
        i += 1
        # add food that must come every period
        for food in list_of_foods:
            if i % food.period == 0:
                # print(f"{i} {food.name} come.")
                food.lastEnter = i
                # print(f"{food.name} enter {food.lastEnter}")
                temp_list.append(food)

    print(f"idle time = {idle_time}.")
    for food in list_of_foods:
        print(f"{food.name} waiting time = {food.waitingTime}.")
    print(f"change between foods is {change_between_foods}.")


def earliest_deadline_first(list_of_foods, chef_time):
    """
    earliest deadline first scheduling algorithm.
    this algorithm priority is minimum deadline between foods.
    in first check if list is empty the chef is idle and increase round and check new foods must come in new round.
    next get food with minimum priority and decrease tempCook and if tempCook is 0 that means the food is done so
    remove the food from list.
    each round decrease tempDeadline and miss food for find use them in predict miss food and find miss food.
    save food in last_food to find changes between foods if last_food is changed and tempCook is not equal to original
    cook time.
    at the end calculate the new foods that must come in new round.
    :param list_of_foods: list of food that chef must cook.
    :param chef_time: maximum time that chef in kitchen.
    :return: nothing return ---> print in terminal
    """
    print(60 * "*")
    print("Earliest deadline first")
    # set value
    for food in list_of_foods:
        food.set_value()
    i = 0
    idle_time = 0
    change_between_foods = 0
    temp_list = list_of_foods.copy()
    last_food = None
    while i < chef_time:

        # check if list is empty print idle and add new foods
        if len(temp_list) == 0:
            print(f"{i} Idle.")
            idle_time += 1
            i += 1
            for food in list_of_foods:
                if i % food.period == 0:
                    # print(f"{i} {food.name} come.")
                    temp_list.append(food)
            continue
        for food in list_of_foods:
            food.set_priority_for_edf()
        # find minimum deadline between foods
        min_food = min(temp_list, key=attrgetter('tempDeadline'))
        # calculate change food
        if i == 0:
            pass
        elif min_food != last_food and last_food.tempCook != last_food.cookTime:
            print(f"Chef change food in round {i}")
            change_between_foods += 1
        # cook that food with minimum deadline
        print(f"{i} {min_food.name}.")
        min_food.tempCook -= 1
        # remove food if it's done
        if min_food.tempCook == 0:
            min_food.predict = False
            min_food.priority = 0
            min_food.tempDeadline = min_food.deadline
            min_food.tempCook = min_food.cookTime
            min_food.missFood = min_food.deadline
            min_food.waitingTime += ((i + 1) - min_food.lastEnter) - min_food.cookTime
            temp_list.remove(min_food)
        # like ageing increase priority each round with -1 deadline
        for food in temp_list:
            # if want to remove ageing ---> only need to comment below line
            food.tempDeadline -= 1
            food.missFood -= 1
            if food.missFood == 0:
                print(f"{i} {food.name} miss the deadline.")
        # set min_food as last_food that we use in calculate change between foods
        last_food = min_food
        # predict miss foods
        predict_miss_deadline(temp_list, i)
        i += 1
        # add food that must come every period
        for food in list_of_foods:
            if i % food.period == 0:
                # print(f"{i} {food.name} come.")
                food.lastEnter = i
                # print(f"{food.name} enter {food.lastEnter}")
                temp_list.append(food)

    print(f"idle time = {idle_time}.")
    for food in list_of_foods:
        print(f"{food.name} waiting time = {food.waitingTime}.")
    print(f"change between foods is {change_between_foods}.")


def get_user_input(list_of_food):
    n = int(input("Enter number of foods:"))
    for num in range(n):
        user_input = input(f"{num + 1} Enter food name, cook time, deadline and period in order: ")
        user_input.replace(",", "")
        user_input = user_input.split(" ")
        user_food = Food(user_input[0], user_input[1], user_input[2], user_input[3])
        list_of_food.append(user_food)
    print(list_of_food)


# ----------------------------------------------------------------------------------------------------------------------
# food1 = Food("Food1", 2, 2, 8)
# food2 = Food("Food2", 1, 3, 4)
# food3 = Food("Food3", 3, 6, 8)
#
# # list for store foods
# arr_of_foods = [food1, food2, food3]
# ----------------------------------------------------------------------------------------------------------------------
# # other input
# food1 = Food("Food1", 1, 4, 8)
# food2 = Food("Food2", 2, 2, 5)
# food3 = Food("Food3", 4, 5, 10)
# food4 = Food("Food4", 2, 3, 40)
# # list for store foods
# arr_of_foods = [food1, food2, food3, food4]

# ----------------------------------------------------------------------------------------------------------------------
# food1 = Food("Food1", 3, 2, 20)
# food2 = Food("Food2", 2, 3, 5)
# food3 = Food("Food3", 2, 6, 10)
#
# # list for store foods
# arr_of_foods = [food1, food2, food3]

# ----------------------------------------------------------------------------------------------------------------------
# food1 = Food("Food1", 3, 7, 20)
# food2 = Food("Food2", 2, 4, 5)
# food3 = Food("Food3", 2, 8, 10)
#
# # list for store foods
# arr_of_foods = [food1, food2, food3]

# ----------------------------------------------------------------------------------------------------------------------
# food1 = Food("Food1", 3, 7, 20)
# food2 = Food("Food2", 2, 4, 5)
# food3 = Food("Food3", 2, 8, 10)
#
# # list for store foods
# arr_of_foods = [food1, food2, food3]

# ----------------------------------------------------------------------------------------------------------------------
# food1 = Food("Food1", 2, 6, 6)
# food2 = Food("Food2", 2, 8, 8)
# food3 = Food("Food3", 3, 10, 10)
#
# # list for store foods
# arr_of_foods = [food1, food2, food3]

# ----------------------------------------------------------------------------------------------------------------------
# get user input
arr_of_foods = []
get_user_input(arr_of_foods)

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
rate_monotonic(arr_of_foods, chef_time_spend)
least_laxity_first(arr_of_foods, chef_time_spend)
