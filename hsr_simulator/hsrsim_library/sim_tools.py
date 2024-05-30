"""Contains functions used to simulate individual and repeated pulls in
Honkai Star Rail for use in various simulator applications.

Also contains a function for printing out percentiles over an array.
"""
import random
import numpy as np


def pull(current_4star_chance, current_5star_chance, five_guarantee,
         four_guarantee, four_featured_odds, five_featured_odds):
    """Based on current draw weights, 50/50 odds, and guarantee status,
    determine the outcome of a single pull.

    Args:
        current_4star_chance (float): The percent chance of drawing a 4*
            entity on this pull.
        current_5star_chance (float): The percent chance of drawing a 5*
            entity on this pull.
        five_guarantee (bool): Whether any drawn 5* will be the featured
            banner character.
        four_guarantee (bool): Whether any drawn 4* will be one of the 
            featured 4*s.
        four_featured_odds (float): If not guaranteed, the percent
            chance that a drawn 4* will be the featured character.
        five_featured_odds (float): If not guaranteed, the percent
            chance that a drawn 5* will be the featured character.

    Returns:
        str: one of "3*", "4*", "featured 4*", "5*", and "featured 5*"
    """
    # Roll a random float between 0 and 100.
    roll = random.uniform(0, 100)

    # Calculate and output roll result and reset rates as needed.
    if roll <= current_5star_chance:
        if five_guarantee or random.uniform(0, 100) <= five_featured_odds:
            return "featured 5*"
        return "5*"
    elif roll <= current_4star_chance:
        # 50/50 to pull featured 4*.
        if four_guarantee or random.uniform(0, 100) <= four_featured_odds:
            return "featured 4*"
        return "4*"
    else:
        return "3*"
    

def run_once(mode, target_number, target_pulls, base_4star_chance,
             base_5star_chance, since_4star, since_5star, five_guarantee,
             four_guarantee, soft_pity_start_4star, soft_pity_start_5star,
             four_featured_odds, five_featured_odds):
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
        base_4star_chance (float): The unmodified chance of pulling a
            4* entity in 1 pull.
        base_5star_chance (float): The unmodified chance of pulling a
            5* entity in 1 pull.
        since_4star (int): The number of pulls since a 4* was last
            obtained, also called 4* pity.
        since_5star (int): The number of pulls since a 5* was last
            obtained, also called 5* pity.
        five_guarantee (bool): Whether the next 5* drawn is guaranteed
            to be the featured banner 5*.
        four_guarantee (bool): Whether the next 4* drawn is guaranteed
            to be on of the featured banner 4*s.
        soft_pity_start_4star (int): The pull before when 4* drop rates
            start increasing.
        soft_pity_start_5star (int): The pull before when 5* drop rates
            start increasing.
        four_featured_odds (float): If not guaranteed, the percent
            chance that a drawn 4* will be the featured character.
        five_featured_odds (float): If not guaranteed, the percent
            chance that a drawn 5* will be the featured character.

    Returns:
        [int, int, int, int, int, int]: [total pulls, number of 3*s,
            number of non-featured 4*s, number of featured 4*s, number
            of non-featured 5*s, number of featured 5*s]
    """
    # Calculate the amount by which rates increase after every draw made
    # after crossing the soft pity thresholds. For all banners, these
    # are about 10 times the base chance.
    #
    # It is necessary to create and modify new variables rather than
    # directly editing the base chances since base rates need to be
    # reset after pulling a 4 or 5 star entity.
    current_5star_chance = base_5star_chance
    pity_increment_5star = base_5star_chance * 10
    current_4star_chance = base_4star_chance
    pity_increment_4star = base_4star_chance * 10

    # Initialize counters to track pull results for this trial.
    total_pulls = 0
    num_3stars = 0
    num_other_4stars = 0
    num_featured_4stars = 0
    num_other_5stars = 0
    num_featured_5stars = 0

    # Pull repeatedly until the mode appropriate stop condition is met.
    while (mode == "to number" and num_featured_5stars < target_number) or \
        (mode == "to pulls" and total_pulls < target_pulls):

        # Update soft pity to reflect current pulls.
        if since_5star >= soft_pity_start_5star:
            current_5star_chance += pity_increment_5star
        if since_4star >= soft_pity_start_4star:
            current_4star_chance += pity_increment_4star

        # Make one pull and update all relevant counters.
        pull_result = pull(current_4star_chance, current_5star_chance, 
                           five_guarantee, four_guarantee, four_featured_odds,
                           five_featured_odds)
        match pull_result:
            case "3*":
                # Increment 4* and 5* pity trackers.
                num_3stars += 1
                since_4star += 1
                since_5star += 1
            case "4*":
                # Increment pity trackers, reset chance, set guarantee.
                num_other_4stars += 1
                since_4star = 0
                since_5star += 1
                current_4star_chance = base_4star_chance
                four_guarantee = True
            case "featured 4*":
                # Increment pity trackers, reset chance, no guarantee.
                num_featured_4stars += 1
                since_4star = 0
                since_5star += 1
                current_4star_chance = base_4star_chance
                four_guarantee = False
            case "5*":
                # Increment pity trackers, reset chance, set guarantee.
                num_other_5stars += 1
                since_4star += 1
                since_5star = 0
                current_5star_chance = base_5star_chance
                five_guarantee = True
            case "featured 5*":
                # Increment pity trackers, reset chance, no guarantee.
                num_featured_5stars += 1
                since_4star += 1
                since_5star = 0
                current_5star_chance = base_5star_chance
                five_guarantee = False

        total_pulls += 1
    
    # Compile and return results.
    results = [total_pulls, 
               num_3stars, 
               num_other_4stars, 
               num_featured_4stars, 
               num_other_5stars, 
               num_featured_5stars]

    return results


def print_percentiles(a):
    """
    Determine a set of percentiles for an array in incremenets of 5,
    including 99% and 100%.

    Args:
        a (array_like): An array of values to calculate and print
        percentile values for.
    """
    # Convert imported list to numpy array type.
    a = np.array(a)
    # Calculate percentiles in increments of 5.
    # Also calculates the 99th and 100th percentiles.
    # This can theoretically be done with a loop to improve
    # maintainability, but why?
    per5 = round(np.percentile(a, 5), 2)
    per10 = round(np.percentile(a, 10), 2)
    per15 = round(np.percentile(a, 15), 2)
    per20 = round(np.percentile(a, 20), 2)
    per25 = round(np.percentile(a, 25), 2)
    per30 = round(np.percentile(a, 30), 2)
    per35 = round(np.percentile(a, 35), 2)
    per40 = round(np.percentile(a, 40), 2)
    per45 = round(np.percentile(a, 45), 2)
    per50 = round(np.percentile(a, 50), 2)
    per55 = round(np.percentile(a, 55), 2)
    per60 = round(np.percentile(a, 60), 2)
    per65 = round(np.percentile(a, 65), 2)
    per70 = round(np.percentile(a, 70), 2)
    per75 = round(np.percentile(a, 75), 2)
    per80 = round(np.percentile(a, 80), 2)
    per85 = round(np.percentile(a, 85), 2)
    per90 = round(np.percentile(a, 90), 2)
    per95 = round(np.percentile(a, 95), 2)
    per99 = round(np.percentile(a, 99), 2)
    per100 = round(np.percentile(a, 100), 2)

    # Print values obtained for all percentiles.
    print("Percentile Cutpoints (Inclusive):")
    print(f" 5% : {per5:^5} | 55% : {per55:^5}")
    print(f"10% : {per10:^5} | 60% : {per60:^5}")
    print(f"15% : {per15:^5} | 65% : {per65:^5}")
    print(f"20% : {per20:^5} | 70% : {per70:^5}")
    print(f"25% : {per25:^5} | 75% : {per75:^5}")
    print(f"30% : {per30:^5} | 80% : {per80:^5}")
    print(f"35% : {per35:^5} | 85% : {per85:^5}")
    print(f"40% : {per40:^5} | 90% : {per90:^5}")
    print(f"45% : {per45:^5} | 95% : {per95:^5}")
    print(f"50% : {per50:^5} | 99% : {per99:^5}")
    print(f"Maximum Value (100%): {per100:^5}")
    print()