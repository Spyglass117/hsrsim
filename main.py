"""This script is intended to repeatedly simulate large numbers of pulls
in the gacha games Honkai Star Rail and Genshin Impact.

DO NOT IMPORT THIS MODULE TO ANOTHER FILE. Most of the functions will
not work correctly outside of this module as they are either set up to
directly reference and edit global state variables or call functions
that do. It is technically possible to use these functions as-is in a
separate module provided you import this entire module and edit the
parameter variables as necessary, but this module is not set up to make
that experience anything less than 'decidedly not fine.'

This breaks encapsulation and is generally an exceedingly poor design
choice, however this is a quick project and the intended method of use
is for the user to hard-code their desired simulation parameters
directly by editing variables. In this case, it is easier to put all
such variables to control the simulation at the top of the file where
they can be quickly changed. This method also cuts down on development
and run time by eliminating the need to collect and clean user inputs
while also enabling simulation parameters to be saved without needing
to manually enter settings at the beginning of each execution.

To use this file, simply edit the variables defined between the end of
this docstring and the first function definition on line 92. Detailed
descriptions of the function of each variable are provided in the
comments below. Take care to enter variables exactly as specified or
the program will not work.

(The only form of error handling is a try catch block wrapping the call
to main)

Examples:
    If in "to pulls" mode with target_pulls set to 100 and multi run set
    to 1000, the system will conduct 100 pulls 1000 times and output the
    average results.

    If in "to number" mode with target_number set to 4 and multi run set
    to 2000, the system will pull until 4 featured 5* characters are
    obtained 2000 times, then output the average pulls required to reach
    the target.

    Note that as explained below, base rates must be manually adjusted
    to simulate a light cone banner rather than a character banner.


Attributes:
    mode (str): The mode of execution. Must be either "to number" or 
        "to pulls" otherwise an exception is raised.
    target_number (int): In "to number" mode, the number of featured 5*
        entities will be drawn in each run before stopping.
    target_pulls (int): In "to pulls" mode, the number of pulls that
        will be made in each run before stopping.
    multi_run (int): The number of runs that will be conducted in total.
    double_top_up (bool): Whether the first purchase bonus is available.
    since_4star (int): The initial draws since last obtaining a 4*.
    since_5star (int): The initial draws since last obtaining a 5*.
    base_4star_chance (int): The base chance of drawing a 4* (percent).
    base_5star_chance (int): The base chance of drawing a 5* (percent).
    cached_base_5star_chance (int): Used to reset the 5* chance after
        drawing a 5* since soft-pity adjustments modify
        base_5star_chance directly. Do not edit this line.
    soft_pity_start (int): The pull before soft pity should kick in.
    soft_pity_increment (int): How much the base chance is adjusted by
        after each additional draw without obtaining a 5*.
    guarantee (bool): Whether the next 5* is guaranteed to be featured.
    featured_odds (float): The odds of winning the "50/50" (percent).
"""
import random
import numpy as np
import matplotlib.pyplot as plot

# Define simulation length. This is essentially the main control panel.
# If mode is set to "to number" the simulation will continue pulling
# until the target_number of featured 5* entities are drawn. 
# If mode is set to "to pulls" the simulation will pull the specified
# specified number of times.
mode = "to number"
target_number = 1
target_pulls = 180

# Decide how many times to run the simulation. If the mode is set to
# "to number" then the simulation will output the average number of warp
# tickets, stellar jade, and dollars required to reach the target number
# of entitites along with other descriptive statistics.
# If the mode is set to "to pulls" then the system will output the
# average number of each class of entity drawn in the specified number
# of pulls.
multi_run = 100000

# Define whether the user can claim double oneiric shards from the shop.
# This is important for calculating rough dollar cost of pulls.
double_top_up = False

# Initialize pity counters at 0. These variables represent the number of
# pulls that have been made so far without obtaining a 4* or 5* entity.
# These may be adjusted to reflect actual starting pity values.
since_4star = 0
since_5star = 0

# Define base chances of pulling a 4* or 5* entity. These rates are for
# each individual pull and are set to 5.1 and 0.6 by default. Change
# these variables to 6.6 and 0.8 to simulate the light cone banner.
base_4star_chance = 5.1
base_5star_chance = 0.6

# Do NOT edit this line. Used to reset 5* chance after drawing a 5*.
# Yes I know this is not best practice. Sue me.
cached_base_5star_chance = base_5star_chance

# Define soft pity information. The variable soft_pity_start is the pull
# immediately BEFORE the 5* rate starts increasing. By default this is
# 73, as the 74th pull is the first pull with an increased rate.
# soft_pity_increment defines how much the rate increases per pull.
soft_pity_start = 73
soft_pity_increment = 6

# Initialize state of 50/50 guarantee. Switch this to True if your next
# 5* is guaranteed to be the featured banner 5*.
guarantee = False

# Define the odds of a drawn 5* being the featured entity. This variable
# represents the 50/50 odds. Change this to 75.0 for light cones.
featured_odds = 56.4




# The variables above are designed to be edited by the end user. As this
# is a quick project, there are no forms of error handling or input
# control built into the program. You are welcome to check out the math
# below, but I advise against editing anything unless you are familiar
# enough with python to know what you are doing.
#
# If you do know enough about python to edit this and feel like putting
# effort into... this. By all means help me optimize and improve it.
def pull():
    """Based on draw weights, 50/50 odds, current pity, and guarantee
    status, determine the outcome of a single pull.

    This function has no arguments as it directly references and
    modifies global level variables. This is the easiest way I could
    find to store pity information between subsequent calls of the pull
    function without needing to return the current pity from each call
    to the function and pass pity information back into the function.

    Returns:
        str: one of "3*", "4*", "featured 4*", "5*", and "featured 5*"
    """
    global since_4star
    global since_5star
    global base_4star_chance
    global base_5star_chance
    global cached_base_5star_chance
    global soft_pity_start
    global soft_pity_increment
    global guarantee
    global featured_odds


    # Update 5* chances based to reflect current soft pity.
    if since_5star >= soft_pity_start:
        base_5star_chance += soft_pity_increment

    # Roll a random float between 0 and 100.
    roll = random.uniform(0.00, 100.00)

    # Calculate and output roll result and reset rates as needed.
    if roll <= base_5star_chance or since_5star == 89:
        since_4star += 1
        since_5star = 0
        base_5star_chance = cached_base_5star_chance
        if random.uniform(0.00, 100.00) <= featured_odds or guarantee:
            # Won 50/50! Next 5* not guaranteed to be featured.
            guarantee = False
            return "featured 5*"
        # Lost 50/50, next 5* guaranteed to be featured.
        guarantee = True
        return "5*"
    elif roll <= base_4star_chance or since_4star == 9:
        since_4star = 0
        since_5star += 1
        # 50/50 to pull featured 4*.
        if random.getrandbits(1):
            return "featured 4*"
        return "4*"
    else:
        since_4star += 1
        since_5star += 1
        return "3*"
    

def dollar_cost(pulls, double_top_up = False):
    """Return the number of dollars needed for the specified pulls.
    
    This function attempts to approximate the dollar cost of buying the
    specified number of pulls. If the first top up bonus is available,
    the function first tries to reach the target number of stellar jade
    by purchasing only packages with a bonus, from least expensive to
    most expensive. After all first top up bonuses are depleted, or if 
    double_top_up is initially set to false, the function will only
    purchase the $99.99 package for the most efficient jade to dollar
    ratio. The function will helpfully output the number of excess jades
    created by only purchasing the most expensive package.

    Args:
        pulls (int): The number of pulls to approximate the cost for.
        double_top_up (bool): Whether the first purchase bonus is
            available. Defaults to False.
        
    Returns:
        [float, int]: [dollar cost of pulls, any leftover jade]
    """
    jade_needed = pulls * 160
    jade_purchased = 0
    cost_of_jade = 0

    while jade_purchased < jade_needed:
        # Make all purchases with jade doubled if available.
        if double_top_up and jade_purchased < jade_needed:
            jade_purchased += 120
            cost_of_jade += 0.99
        if double_top_up and jade_purchased < jade_needed:
            jade_purchased += 600
            cost_of_jade += 4.99
        if double_top_up and jade_purchased < jade_needed:
            jade_purchased += 1960
            cost_of_jade += 14.99
        if double_top_up and jade_purchased < jade_needed:
            jade_purchased += 3960
            cost_of_jade += 29.99
        if double_top_up and jade_purchased < jade_needed:
            jade_purchased += 6560
            cost_of_jade += 49.99
        if double_top_up and jade_purchased < jade_needed:
            jade_purchased += 12960
            cost_of_jade += 99.99
            double_top_up = False
        # If all double bonuses used, continues purchasing $100 package.
        if jade_purchased < jade_needed:
            jade_purchased += 8080
            cost_of_jade += 99.99

    leftover_jade = jade_purchased - jade_needed
    cost_of_jade = round(cost_of_jade, 2)
    return [cost_of_jade, leftover_jade]


def run_once(mode = "to pulls", target_number = 1, target_pulls = 90):
    """Run one trial of the simulation, terminating when either the
    target number of featured 5*s are drawn or when the target pulls are
    reached, depending on the mode selected.

    Args:
        mode (str): The mode of execution. Must be either "to number" or 
            "to pulls" otherwise an exception is raised.
        target_number (int): In "to number" mode, the number of featured
            5* entities will be drawn before returning results.
        target_pulls (int): In "to pulls" mode, the number of pulls that
            will be made before returning results.

    Returns:
        [int, int, int, int, int, int]: [total pulls, number of 3*s,
            number of non-featured 4*s, number of featured 4*s, number
            of non-featured 5*s, number of featured 5*s]
    """
    total_pulls = 0

    num_3stars = 0
    num_other_4stars = 0
    num_featured_4stars = 0
    num_other_5stars = 0
    num_featured_5stars = 0

    if mode == "to number":
        while True:
            # Make one pull and update total counters.
            pull_result = pull()
            match pull_result:
                case "3*":
                    num_3stars += 1
                case "4*":
                    num_other_4stars += 1
                case "featured 4*":
                    num_featured_4stars += 1
                case "5*":
                    num_other_5stars += 1
                case "featured 5*":
                    num_featured_5stars += 1

            total_pulls += 1

            # Stop pulling if all requested entities are pulled.
            if num_featured_5stars >= target_number:
                break

    if mode == "to pulls":
        while True:
            # Make one pull and update total counters.
            pull_result = pull()
            match pull_result:
                case "3*":
                    num_3stars += 1
                case "4*":
                    num_other_4stars += 1
                case "featured 4*":
                    num_featured_4stars += 1
                case "5*":
                    num_other_5stars += 1
                case "featured 5*":
                    num_featured_5stars += 1

            total_pulls += 1

            # Stop pulling after the target number of pulls.
            if total_pulls >= target_pulls:
                break

    results = [total_pulls, 
               num_3stars, 
               num_other_4stars, 
               num_featured_4stars, 
               num_other_5stars, 
               num_featured_5stars]

    return results


def main(mode, target_number, target_pulls, multi_run):
    """Carry out multi_run trials in the specified mode. 
    
    Refer to the module docstring for documentation of the main method.
    """
    # Declare variables and report paramaters to user.
    print(f"Initializing simulator in \"{mode}\" mode.")
    if mode == "to number":
        print(f"System will draw: {target_number} featured 5*s per trial")
    elif mode == "to pulls":
        print(f"System will draw: {target_pulls} pulls per trial.")
    else:
        print("Mode not recognized. Execution halted.")
        return
    print(f"Simulation will terminate after: {multi_run} trials")
    print("Loading simulation parameters...", end = "")

    global since_4star
    global since_5star
    global base_4star_chance
    global base_5star_chance
    global guarantee
    global featured_odds
    global double_top_up

    print(f"{'...done':>20}")
    print()

    print(f"Initial draws since last 4* (pity): {since_4star}")
    print(f"Initial draws since last 5* (pity): {since_5star}")
    print(f"Base chance to draw a 4* entity: {base_4star_chance}")
    print(f"Base chance to draw a 5* entity: {base_5star_chance}")
    print(f"Initial next 5* guaranteed to be featured: {guarantee}")
    print(f"Chance of winning banner 5* w/o guarantee: {featured_odds}/100")
    print(f"First top-up bonus available in store: {double_top_up}")
    print()

    # Initialize empty lists to hold results for each run.
    print("Initializing data containers...", end = "")
    running_total_pulls = []
    running_num_3stars = []
    running_num_other_4stars = []
    running_num_featured_4stars = []
    running_num_other_5stars = []
    running_num_featured_5stars = []
    print(f"{'...done':>21}")

    # Collect data over specified number of runs.
    print("Running simulations (this may take time)...", end = "")
    for run in range(multi_run):
        run_result = run_once(mode, target_number, target_pulls)
        running_total_pulls.append(run_result[0])
        running_num_3stars.append(run_result[1])
        running_num_other_4stars.append(run_result[2])
        running_num_featured_4stars.append(run_result[3])
        running_num_other_5stars.append(run_result[4])
        running_num_featured_5stars.append(run_result[5])
    print(f"{'...done':>9}")

    # Calculate statistics for output.
    print("Calculating statistics...", end = "")
    # Calculate pull and cost statistics for output.
    mean_pulls = round(np.mean(running_total_pulls), 2)
    # Stdev will raise an exception if only 1 data point is supplied.
    # This works fine for the scope of this project.
    if multi_run > 1:
        stdev_pulls = round(np.std(running_total_pulls), 2)
    else:
        stdev_pulls = "N/A"
    max_pulls = max(running_total_pulls)
    min_pulls = min(running_total_pulls)
    jade_cost_mean = round(mean_pulls) * 160
    jade_cost_max = max_pulls * 160
    jade_cost_min = min_pulls * 160
    dollar_cost_mean = dollar_cost(round(mean_pulls), double_top_up)[0]
    dollar_cost_max = dollar_cost(max_pulls, double_top_up)[0]
    dollar_cost_min = dollar_cost(min_pulls, double_top_up)[0]
    leftover_mean = dollar_cost(round(mean_pulls), double_top_up)[1]
    leftover_max = dollar_cost(max_pulls, double_top_up)[1]
    leftover_min = dollar_cost(min_pulls, double_top_up)[1]

    # Calculate pull results statistics for output.
    mean_num_3stars = np.mean(running_num_3stars)
    mean_num_3stars = round(mean_num_3stars, 2)
    mean_num_other_4stars = np.mean(running_num_other_4stars)
    mean_num_other_4stars = round(mean_num_other_4stars, 2)
    mean_num_featured_4stars = np.mean(running_num_featured_4stars)
    mean_num_featured_4stars = round(mean_num_featured_4stars, 2)
    mean_num_other_5stars = np.mean(running_num_other_5stars)
    mean_num_other_5stars = round(mean_num_other_5stars, 2)
    mean_num_featured_5stars = np.mean(running_num_featured_5stars)
    mean_num_featured_5stars = round(mean_num_featured_5stars)
    print(f"{'...done':>27}")
    print()

    # Compile and format mode appropriate results and output to user.
    if mode == "to number":
        print(f"The mean number of pulls to obtain {target_number} of the " 
              f"featured 5* over {multi_run} trials is {mean_pulls} with a "
              f"standard deviation of {stdev_pulls}.")
        print(f"{target_number} copies of the featured 5* were drawn in as few"
              f" as {min_pulls} pulls and as many as {max_pulls} pulls.")
        print("Note that as the number of trials increases min pulls will "
              "trend lower and max pulls will trend higher.")
        print()
        print("The approximate costs for the minimum, mean, and maximum "
              f"number of pulls estimated to reach {target_number} copies of "
              "the featured 5* are:")
    if mode == "to pulls":
        print(f"The approximate costs for {target_pulls} pulls are:")
    print(f"{'':<15}{'Pulls':^15}{'Jade Cost':^15}"
          f"{'Dollar Cost':^15}{'Excess Jade':^15}")
    print(f"{'Minimum Case':<15}{min_pulls:^15}{jade_cost_min:^15}"
          f"{dollar_cost_min:^15}{leftover_min:^15}")
    print(f"{'Mean Case':<15}{mean_pulls:^15}{jade_cost_mean:^15}"
          f"{dollar_cost_mean:^15}{leftover_mean:^15}")
    print(f"{'Maximum Case':<15}{max_pulls:^15}{jade_cost_max:^15}"
          f"{dollar_cost_max:^15}{leftover_max:^15}")
    print()

    print(f"The mean rarity distribution for {mean_pulls} pulls over " 
          f"{multi_run} trials is:")
    print(f"{'Category':<15}{'Quantity':^15}")
    print(f"{'3*':<15}{mean_num_3stars:^15}")
    print(f"{'Non-featured 4*':<15}{mean_num_other_4stars:^15}")
    print(f"{'Featured 4*':<15}{mean_num_featured_4stars:^15}")
    print(f"{'Non-featured 5*':<15}{mean_num_other_5stars:^15}")
    print(f"{'Featured 5*':<15}{mean_num_featured_5stars:^15}")
    print()

    # Assemble and output a histogram showing pull distribution to aid
    # in data visualization. 
    pull_data = running_total_pulls
    plot.hist(pull_data, 
              bins=np.arange(min(pull_data), max(pull_data) + 1, 1))
    plot.show()

try:
    main(mode, target_number, target_pulls, multi_run)
except Exception:
    print("Program execution halted due to exception.")
    print("This is a default error handling message indicating that "
          "something may have gone wrong somewhere in the program")
    print("Most probably this is your fault; check your parameters as "
          "well as any changes you may have made to the code.")
    print("Please note that this has not been rigourously tested.")
    print("Message me on Reddit at u/Fliegermaus if the issue persists.")

# I did this for you Queen Firefly! Please come home; I love you.