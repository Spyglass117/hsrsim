"""This script is intended to repeatedly simulate large numbers of pulls
in the game Honkai Star Rail using a pseduo-random Monte Carlo method.

To use this file, simply edit the variables defined between the end of
this docstring and the first function definition on line 190 and press
run. Detailed descriptions of the function of each variable are provided
above each one below. Take care to enter variables exactly as specified
or the program will not work as expected. Please note that there is no
robust error handling framework in place; entering an invalid value will
simply raise an exception and terminate the program.

Each call to the main method will run a number of trials equal to
the 'multi_run' parameter. Each trial terminates when a condition set
by the 'mode' parameter is met. In "to pulls" mode, each trial will
stop after reaching the number of pulls specified by the
'target_pulls' parameter. In "to number" mode, each trial will stop
after reaching the 'target_number' of copies of the featured 5*.

In "to pulls" mode, only a distribution of the rarities and types of
the various entities gained on average over the specified pulls. In
"to number" mode, This data will only be provided for the mean
number of pulls required to reach the target number. "to number"
mode will also output the minimum, maximum, mean, and standard
deviation of the pull totals from all trials as well as percentiles
showing what percentage of simulations ended at of before a certain
pull. Both modes will output cost estimates in stellar jade and US
dollars to purchase the minimum, maximum, and mean pulls as well as
a rough estimate of the amount of stardust gained from making the
mean number of pulls.

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
    target_number (int): In "to number" mode, the number of featured
        5* entities will be drawn before returning results.
    target_pulls (int): In "to pulls" mode, the number of pulls that
        will be made before returning results.
    multi_run (int): The number of trials to run before stopping.
    base_4star_chance (float): The unmodified chance of pulling a
        4* entity in 1 pull (percent).
    base_5star_chance (float): The unmodified chance of pulling a
        5* entity in 1 pull (percent).
    since_4star (int): The number of pulls since a 4* was last
        obtained, also called 4* pity.
    since_5star (int): The number of pulls since a 5* was last
        obtained, also called 5* pity.
    five_guarantee (bool): Whether the next 5* drawn is guaranteed to be
        the featured banner 5*.
    four_guarantee (bool): Whether the next 4* drawn is guaranteed to be
        one of the featured banner characters.
    saved_pulls (int): The number of pulls the user already has.
    soft_pity_start_4star (int): The pull before when 4* drop rates
        start increasing.
    soft_pity_start_5star (int): The pull before when 5* drop rates
        start increasing.
    featured_odds (float): The chances of pulling a featured 5*
        instead of a standard 5* (percent). "50/50" odds.
    double_top_up (bool): Whether the first purchase bonus is
        available. Defaults to False.
    e_mode (bool): If False, attempts to minimize the dollar cost of
        purchased jade even if doing so would be less efficient than
        purchasing a more expensive package. If True, after using up
        all double top up packcages, only purchases the $99.99
        package. Defaults to False.
    owned_4stars (int): The number of 4* entities already owned.
    e6_4stars (int): The number of 4* characters at e6.
    owned_standard_5stars (int): The number of standard banner 5*
        entities already owned.
    e6_5stars (int): The number of standard 5* characters at e6.
    owned_feat1 (int): The number of copies of the first featured 4*
        already owned by the user.
    owned_feat2 (int): The number of copies of the second featured
        4* already owned by the user.
    owned_feat3 (int): The number of copies of the third featured 4*
        already owned by the user.
    banner_type (str): Either "character" or "light cone". Used in
        estimating stardust, and only in estimating stardust.
"""
import math
import numpy as np
import matplotlib.pyplot as plot
from hsrsim_library.sim_tools import run_once, print_percentiles
from hsrsim_library.sim_calculators import dollar_cost, estimate_stardust

# Define simulation length. This is essentially the main control panel.
# If mode is set to "to number" in each trial the simulation will
# continue pulling until the target_number of featured 5* entities are 
# drawn. If mode is set to "to pulls" in each trial the simulation will
# pull the specified number of times.
mode = "to pulls"
target_number = 1
target_pulls = 90

# Decide how many times to run the simulation. This is the number of
# trials the system will conduct before stopping. If the mode is set to
# "to number" then the simulation will output the average number of warp
# tickets, stellar jade, and dollars required to reach the target number
# of entitites along with other descriptive statistics.
# If the mode is set to "to pulls" then the system will output the
# average number of each class of entity drawn in the specified number
# of pulls.
multi_run = 100000

# These variables represent the number of pulls that have been made so
# far without obtaining a 4* or 5* entity. These may be adjusted to
# reflect actual starting pity values. By default both are 0.
since_4star = 0
since_5star = 0

# Initialize state of 50/50 guarantee. Switch five_guarantee to True if
# your next 5* is guaranteed to be the featured banner 5*. Switch
# four_guarantee to True if your next 4* is guaranteed to be one of the
# featured banner 4*s.
five_guarantee = False
four_guarantee = False

# Define whether the user can claim double oneiric shards from the shop.
# This is important for calculating the rough dollar cost of pulls.
double_top_up = False

# Whether jade should only be purchased at the most favorable exchange
# ratio. When calculating the dollar cost of pulls, this setting will
# prioritize double_top_up packages if available, then only purchase the
# $99.99 package.
e_mode = False

# The number of saved pulls the user has. This will modify the costs in
# the output by reducing the number of pulls that need to be purchased.
saved_pulls = 0

# The number of 4* and standard banner units the user already owns. This
# is used for a VERY ROUGH ESTIMATE of pulls gained from starlight.
# Also indicate the number of E6 characters owned for each type.
owned_4stars = 0
e6_4stars = 0
owned_standard_5stars = 0
e6_5stars = 0

# The number of each featured 4* already owned. Note that this should be
# the number of COPIES of a character rather than the eidolon level. For
# example if a character is at E4, enter 5. It does not matter what
# order characters are entered in, this is only used for starlight
# calculations.
owned_feat1 = 0
owned_feat2 = 0
owned_feat3 = 0

# This is only used for starlight estimation; the probability and pity
# information below must still be edited to simulate the light cone
# banner. Set this variable to "character" to estimate starlight drops
# on the character banner, or "light cone" for the light cone banner.
banner_type = "character"

# Define base chances of pulling a 4* or 5* entity. These rates are for
# each individual pull and are set to 5.1 and 0.6 by default. Change
# these variables to 6.6 and 0.8 to simulate the light cone banner.
base_4star_chance = 5.1
base_5star_chance = 0.6

# Define soft pity information. These should be set to the pull
# immediately BEFORE the rate starts increasing. These should be 8 and
# 73 for character banners and 7 and 65 for light cone banners.
soft_pity_start_4star = 8
soft_pity_start_5star = 73

# Define the odds of a drawn 5* being the featured entity. This variable
# represents the "50/50" odds. Change this to 75.0 for light cones.
# By default this is 56.4 to reflect pull data.
featured_odds = 56.4




# The variables above are designed to be edited by the end user. There
# is limited error handling or input checking. You are welcome to check
# out the code below, but I advise against editing anything unless you
# are familiar enough with python to know what you are doing.
#
# If you do know enough about python to edit this and feel like putting
# effort into... this. By all means help me optimize and improve it.
def main(mode, target_number, target_pulls, multi_run, base_4star_chance,
         base_5star_chance, since_4star, since_5star, five_guarantee,
         four_guarantee, saved_pulls, soft_pity_start_4star,
         soft_pity_start_5star, featured_odds, double_top_up, e_mode,
         owned_4stars, e6_4stars, owned_standard_5stars, e6_5stars,
         owned_feat1, owned_feat2, owned_feat3, banner_type):
    """Conduct repeated Monte Carlo simulations of multiple HSR draws.

    Each call to the main method will run a number of trials equal to
    the 'multi_run' parameter. Each trial terminates when a condition set
    by the 'mode' parameter is met. In "to pulls" mode, each trial will
    stop after reaching the number of pulls specified by the
    'target_pulls' parameter. In "to number" mode, each trial will stop
    after reaching the 'target_number' of copies of the featured 5*.

    In "to pulls" mode, only a distribution of the rarities and types of
    the various entities gained on average over the specified pulls. In
    "to number" mode, This data will only be provided for the mean
    number of pulls required to reach the target number. "to number"
    mode will also output the minimum, maximum, mean, and standard
    deviation of the pull totals from all trials as well as percentiles
    showing what percentage of simulations ended at of before a certain
    pull. Both modes will output cost estimates in stellar jade and US
    dollars to purchase the minimum, maximum, and mean pulls as well as
    a rough estimate of the amount of stardust gained from making the
    mean number of pulls.

    Refer to the module docstring for documentation on the use of the
    main method in the context of the HSR Simulator script.

    Examples:
        If in "to pulls" mode with target_pulls set to 100 and multi run
        set to 1000, the system will conduct 100 pulls 1000 times and
        output the average results, cost, and stardust.

        If in "to number" mode with target_number set to 4 and multi run
        set to 2000, the system will pull until 4 featured 5* characters
        are obtained 2000 times, then output the average pulls required
        to reach the target, average results, cost, stardust, and
        percentiles.

        Note that as explained below, base rates must be manually adjusted
        to simulate a light cone banner rather than a character banner.
    
    Args:
        mode (str): The mode of execution. Must be either "to number" or 
            "to pulls" otherwise an exception is raised.
        target_number (int): In "to number" mode, the number of featured
            5* entities will be drawn before returning results.
        target_pulls (int): In "to pulls" mode, the number of pulls that
            will be made before returning results.
        multi_run (int): The number of trials to run before stopping.
        base_4star_chance (float): The unmodified chance of pulling a
            4* entity in 1 pull (percent).
        base_5star_chance (float): The unmodified chance of pulling a
            5* entity in 1 pull (percent).
        since_4star (int): The number of pulls since a 4* was last
            obtained, also called 4* pity.
        since_5star (int): The number of pulls since a 5* was last
            obtained, also called 5* pity.
        five_guarantee (bool): Whether the next 5* drawn is guaranteed to be
            the featured banner 5*.
        four_guarantee (bool): Whether the next 4* drawn is guaranteed to be
            one of the featured banner characters.
        saved_pulls (int): The number of pulls the user already has.
        soft_pity_start_4star (int): The pull before when 4* drop rates
            start increasing.
        soft_pity_start_5star (int): The pull before when 5* drop rates
            start increasing.
        featured_odds (float): The chances of pulling a featured 5*
            instead of a standard 5* (percent). "50/50" odds.
        double_top_up (bool): Whether the first purchase bonus is
            available. Defaults to False.
        e_mode (bool): If False, attempts to minimize the dollar cost of
            purchased jade even if doing so would be less efficient than
            purchasing a more expensive package. If True, after using up
            all double top up packcages, only purchases the $99.99
            package. Defaults to False.
        owned_4stars (int): The number of 4* entities already owned.
        e6_4stars (int): The number of 4* characters at e6.
        owned_standard_5stars (int): The number of standard banner 5*
            entities already owned.
        e6_5stars (int): The number of standard 5* characters at e6.
        owned_feat1 (int): The number of copies of the first featured 4*
            already owned by the user.
        owned_feat2 (int): The number of copies of the second featured
            4* already owned by the user.
        owned_feat3 (int): The number of copies of the third featured 4*
            already owned by the user.
        banner_type (str): Either "character" or "light cone". Used in
            estimating stardust, and only in estimating stardust.
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
    print(f"{'...done':>20}")
    print()

    print(f"Initial draws since last 4* (pity): {since_4star}")
    print(f"Initial draws since last 5* (pity): {since_5star}")
    print(f"Base chance to draw a 4* entity: {base_4star_chance}")
    print(f"Base chance to draw a 5* entity: {base_5star_chance}")
    print(f"4* soft pity starting after: {soft_pity_start_4star}")
    print(f"5* soft pity starting after: {soft_pity_start_5star}")
    print(f"Initial next 5* guaranteed to be featured: {five_guarantee}")
    print(f"Initial next 4* guaranteed to be featured: {four_guarantee}")
    print(f"Chance of winning banner 5* w/o guarantee: {featured_odds}/100")
    print(f"Pulls already saved for banner: {saved_pulls}")
    print(f"First top-up bonus available in store: {double_top_up}")
    print(f"Purchase jade at best exchange rate: {e_mode}")
    print(f"#/E6 4*|#/E6 5*: "
          f"{owned_4stars}/{e6_4stars}|{owned_standard_5stars}/{e6_5stars}")
    print(f"Owned banner 4* 1/2/3: {owned_feat1}/{owned_feat2}/{owned_feat3}")
    print(f"Banner type for stardust estimation: {banner_type}")
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
        run_result = run_once(mode, target_number, target_pulls,
                              base_4star_chance, base_5star_chance,
                              since_4star, since_5star, five_guarantee, 
                              four_guarantee, soft_pity_start_4star, 
                              soft_pity_start_5star, featured_odds)
        running_total_pulls.append(run_result[0])
        running_num_3stars.append(run_result[1])
        running_num_other_4stars.append(run_result[2])
        running_num_featured_4stars.append(run_result[3])
        running_num_other_5stars.append(run_result[4])
        running_num_featured_5stars.append(run_result[5])
    print(f"{'...done':>9}")

    # Calculate statistics for output.
    print("Calculating statistics...", end = "")
    # Calculate pull statistics.
    mean_pulls = round(np.mean(running_total_pulls), 2)
    mean_pulls_needed = int(math.ceil(max(mean_pulls - saved_pulls, 0)))
    max_pulls = max(running_total_pulls)
    max_pulls_needed = max(max_pulls - saved_pulls, 0)
    min_pulls = min(running_total_pulls)
    min_pulls_needed = max(min_pulls - saved_pulls, 0)
    # Stdev will raise an exception if only 1 data point is supplied.
    # This works fine for the scope of this project.
    if multi_run > 1:
        stdev_pulls = round(np.std(running_total_pulls, ddof = 1), 2)
    else:
        stdev_pulls = "N/A"
    # Calculate cost of pulls in stellar jade and USD.
    jade_cost_mean = round(mean_pulls_needed) * 160
    jade_cost_max = max_pulls_needed * 160
    jade_cost_min = min_pulls_needed * 160
    raw_dc_mean = dollar_cost(round(mean_pulls_needed), double_top_up, e_mode)
    raw_dc_max = dollar_cost(max_pulls_needed, double_top_up, e_mode)
    raw_dc_min = dollar_cost(min_pulls_needed, double_top_up, e_mode)
    dollar_cost_mean = raw_dc_mean[0]
    dollar_cost_max = raw_dc_max[0]
    dollar_cost_min = raw_dc_min[0]
    leftover_mean = raw_dc_mean[1]
    leftover_max = raw_dc_max[1]
    leftover_min = raw_dc_min[1]

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
        # Some statistics only make sense in to number mode.
        print(f"The mean number of pulls to obtain {target_number} of the " 
              f"featured 5* over {multi_run} trials is {mean_pulls} with a "
              f"standard deviation of {stdev_pulls}.")
        print(f"{target_number} copies of the featured 5* were drawn in as few"
              f" as {min_pulls} pulls and as many as {max_pulls} pulls.")
        print("Note that as the number of trials increases min pulls will "
              "trend lower and max pulls will trend higher.")
        print()
        print("The approximate costs* for the minimum, mean, and maximum "
              f"number of pulls estimated to reach {target_number} copies of "
              "the featured 5* are:")
    if mode == "to pulls":
        print(f"The approximate costs for {target_pulls} pulls are:")
    # Cost data is output regardless of mode.
    print(f"{'':<15}{'Total Pulls':^15}{'Missing Pulls':^15}"
          f"{'Jade Cost':^15}{'Dollar Cost':^15}{'Excess Jade':^15}")
    print(f"{'Minimum Case':<15}{min_pulls:^15}{min_pulls_needed:^15}"
          f"{jade_cost_min:^15}{dollar_cost_min:^15}{leftover_min:^15}")
    print(f"{'Mean Case':<15}{mean_pulls:^15}{mean_pulls_needed:^15}"
          f"{jade_cost_mean:^15}{dollar_cost_mean:^15}{leftover_mean:^15}")
    print(f"{'Maximum Case':<15}{max_pulls:^15}{max_pulls_needed:^15}"
          f"{jade_cost_max:^15}{dollar_cost_max:^15}{leftover_max:^15}")
    print("*costs are based on the missing pulls column, which is the "
          "total pulls needed minus the number of saved pulls.")
    print()
    # Rarity distribution of entities output is also mode independent.
    print(f"The mean rarity distribution for {mean_pulls} pulls over " 
          f"{multi_run} trials is:")
    print(f"{'Category':<15}{'Quantity':^15}")
    print(f"{'3*':<15}{mean_num_3stars:^15}")
    print(f"{'Non-featured 4*':<15}{mean_num_other_4stars:^15}")
    print(f"{'Featured 4*':<15}{mean_num_featured_4stars:^15}")
    print(f"{'Non-featured 5*':<15}{mean_num_other_5stars:^15}")
    print(f"{'Featured 5*':<15}{mean_num_featured_5stars:^15}")
    print()
    # Finally, stardust gain is mode independent.
    mean_data = [mean_pulls, mean_num_3stars, mean_num_other_4stars,
                 mean_num_featured_4stars, mean_num_other_5stars,
                 mean_num_featured_5stars]
    estimated_dust = estimate_stardust(mean_data, owned_4stars, 
                                       owned_standard_5stars, e6_4stars,
                                       e6_5stars, owned_feat1, owned_feat2,
                                       owned_feat3, banner_type)
    dust, pulls, remaining_dust = estimated_dust
    print(f"Estimated stardust gains from {mean_pulls} pulls is:")
    print(f"{'Dust':^15}{'Pulls':^15}{'Remaining Dust':^15}")
    print(f"{dust:^15}{pulls:^15}{remaining_dust:^15}")
    print()

    if mode == "to number":
        # Percentiles are output for the chance of reaching the target
        # number of copies within x pulls.
        print("P% of simulations ended within n pulls:")
        print_percentiles(running_total_pulls)

        # Assemble and output a histogram showing pull distribution to
        # aid in data visualization. This outputs a blank graph if all
        # scores are the same number, hence it is only called in to
        # number mode.
        pull_data = running_total_pulls
        plot.hist(pull_data, 
                bins=np.arange(min(pull_data), max(pull_data) + 1, 1))
        plot.show()
    if mode == "to pulls":
        print("P% of simulations ended with n or fewer featured 5*s:")
        print_percentiles(running_num_featured_5stars)


if __name__ == "__main__":
    try:
        main(mode, target_number, target_pulls, multi_run, base_4star_chance,
            base_5star_chance, since_4star, since_5star, five_guarantee, 
            four_guarantee, saved_pulls, soft_pity_start_4star,
            soft_pity_start_5star, featured_odds, double_top_up, e_mode,
            owned_4stars, e6_4stars, owned_standard_5stars, e6_5stars, 
            owned_feat1, owned_feat2, owned_feat3, banner_type)
    except Exception:
        print("Program execution halted due to exception.")
        print("This is a default error handling message indicating that "
              "something may have gone wrong somewhere in the program.")
        print("Most probably this is your fault; check your parameters as "
              "well as any changes you may have made to the code.")
        print("Please note that this has not been rigourously tested.")
        print("Message me on Reddit at u/Fliegermaus if the issue persists.")

# I did this for you Queen Firefly! Please come home; I love you.