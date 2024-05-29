"""This script is used to generate percentile tables illustrating the
number of pulls that would be needed to reach a certain "level" of an on
-banner and off-banner 4* character. Tables are generated for E0 to E6
under both conditions.

This script uses the same code and methodology as the main simulator,
but is significantly less flexible and user friendly as all simulation
parameters are hard-coded into the main method. It is included in this
directory to document and publicize how the published tables were
generated.

The code for this particular module was written under the influence of
sake and may not reflect the "quality standards" demonstrated elsewhere
in this repo.
"""
import random
from sim_tools import pull, print_percentiles


def run_till_on_banner_4star(copies, base_4star_chance = 5.1,
                             base_5star_chance = 0.6,
                             since_4star = 0, since_5star = 0,
                             soft_pity_start_4star = 8,
                             soft_pity_start_5star = 73,
                             featured_odds = 56.4,
                             five_guarantee = False, four_guarantee = False):
    """Simulate pulling until the specified number of copies of an on
    banner featured 4* entity are obtained.

    Args:
        copies (int): The number of copies of the 4* to pull until.
        base_4star_chance (float): The unmodified chance of pulling a
            4* entity in 1 pull.
        base_5star_chance (float): The unmodified chance of pulling a
            5* entity in 1 pull.
        since_4star (int): The number of pulls since a 4* was last
            obtained, also called 4* pity.
        since_5star (int): The number of pulls since a 5* was last
            obtained, also called 5* pity.
        soft_pity_start_4star (int): The pull before when 4* drop rates
            start increasing.
        soft_pity_start_5star (int): The pull before when 5* drop rates
            start increasing.
        featured_odds (float): The chances of pulling a featured 5*
            instead of a standard 5*. Represents 50/50 or 75/25 odds.
        five_guarantee (bool): Whether the next 5* drawn is guaranteed
            to be the featured banner 5*.
        four_guarantee (bool): Whether the next 4* drawn is guaranteed
            to be on of the featured banner 4*s.

    Returns:
        int: The number of pulls needed to reach the target number
            of the target 4* character in this run.
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
    num_target_4stars = 0

    # Pull repeatedly until the target number of featured 4*s is met.
    while num_target_4stars < copies:

        # Update soft pity to reflect current pulls.
        if since_5star >= soft_pity_start_5star:
            current_5star_chance += pity_increment_5star
        if since_4star >= soft_pity_start_4star:
            current_4star_chance += pity_increment_4star

        # Make one pull and update all relevant counters.
        pull_result = pull(current_4star_chance, current_5star_chance, 
                           five_guarantee, four_guarantee, featured_odds)
        match pull_result:
            case "3*":
                # Increment 4* and 5* pity trackers.
                since_4star += 1
                since_5star += 1
            case "4*":
                # Increment pity trackers, reset chance, set guarantee.
                since_4star = 0
                since_5star += 1
                current_4star_chance = base_4star_chance
                four_guarantee = True
            case "featured 4*":
                # Increment pity trackers, reset chance, no guarantee.
                if random.uniform(0, 100) <= (33.33333333333333):
                    num_target_4stars += 1
                since_4star = 0
                since_5star += 1
                current_4star_chance = base_4star_chance
                four_guarantee = False
            case "5*":
                # Increment pity trackers, reset chance, set guarantee.
                since_4star += 1
                since_5star = 0
                current_5star_chance = base_5star_chance
                five_guarantee = True
            case "featured 5*":
                # Increment pity trackers, reset chance, no guarantee.
                since_4star += 1
                since_5star = 0
                current_5star_chance = base_5star_chance
                five_guarantee = False

        total_pulls += 1
    
    return total_pulls


def run_till_off_banner_4star(copies, base_4star_chance = 5.1,
                              base_5star_chance = 0.6,
                              since_4star = 0, since_5star = 0,
                              soft_pity_start_4star = 8,
                              soft_pity_start_5star = 73,
                              featured_odds = 56.4,
                              five_guarantee = False, four_guarantee = False,
                              total_4star_chars = 21, total_4star_cones = 21):
    """Simulate pulling until the specified number of copies of an on
    banner featured 4* entity are obtained.

    Args:
        copies (int): The number of copies of the 4* to pull until.
        base_4star_chance (float): The unmodified chance of pulling a
            4* entity in 1 pull.
        base_5star_chance (float): The unmodified chance of pulling a
            5* entity in 1 pull.
        since_4star (int): The number of pulls since a 4* was last
            obtained, also called 4* pity.
        since_5star (int): The number of pulls since a 5* was last
            obtained, also called 5* pity.
        soft_pity_start_4star (int): The pull before when 4* drop rates
            start increasing.
        soft_pity_start_5star (int): The pull before when 5* drop rates
            start increasing.
        featured_odds (float): The chances of pulling a featured 5*
            instead of a standard 5*. Represents 50/50 or 75/25 odds.
        five_guarantee (bool): Whether the next 5* drawn is guaranteed
            to be the featured banner 5*.
        four_guarantee (bool): Whether the next 4* drawn is guaranteed
            to be on of the featured banner 4*s.
        total_4star_chars (int): The total number of 4* characters
            available on the banner.
        total_4star_cones (int): The total number of 4* light cones
            available on the banner.

        Returns:
            int: The number of pulls needed to reach the target number
                of the target 4* character in this run.
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

    # Calculate chances of non featured 4* being target 4*.
    total_4stars = total_4star_chars + total_4star_cones
    target_chance = (1/total_4stars) * 100

    # Initialize counters to track pull results for this trial.
    total_pulls = 0
    num_target_4stars = 0

    # Pull repeatedly until the target number of featured 4*s is met.
    while num_target_4stars < copies:

        # Update soft pity to reflect current pulls.
        if since_5star >= soft_pity_start_5star:
            current_5star_chance += pity_increment_5star
        if since_4star >= soft_pity_start_4star:
            current_4star_chance += pity_increment_4star

        # Make one pull and update all relevant counters.
        pull_result = pull(current_4star_chance, current_5star_chance, 
                           five_guarantee, four_guarantee, featured_odds)
        match pull_result:
            case "3*":
                # Increment 4* and 5* pity trackers.
                since_4star += 1
                since_5star += 1
            case "4*":
                # Increment pity trackers, reset chance, set guarantee.
                if random.uniform(0, 100) <= target_chance:
                    num_target_4stars += 1
                since_4star = 0
                since_5star += 1
                current_4star_chance = base_4star_chance
                four_guarantee = True
            case "featured 4*":
                # Increment pity trackers, reset chance, no guarantee.
                since_4star = 0
                since_5star += 1
                current_4star_chance = base_4star_chance
                four_guarantee = False
            case "5*":
                # Increment pity trackers, reset chance, set guarantee.
                since_4star += 1
                since_5star = 0
                current_5star_chance = base_5star_chance
                five_guarantee = True
            case "featured 5*":
                # Increment pity trackers, reset chance, no guarantee.
                since_4star += 1
                since_5star = 0
                current_5star_chance = base_5star_chance
                five_guarantee = False

        total_pulls += 1
    
    return total_pulls


def main():
    """Refer to module docstring for main method documentation.
    """
    def simulate_on_banner(copies):
        # Helper function to repeatedly simulate pulling the specified
        # copies of the target on banner 4* and return a list to be
        # passed to print_percentiles().
        running_total_pulls = []
        for run in range(100000):
            running_total_pulls.append(run_till_on_banner_4star(copies))
        return running_total_pulls
    
    def simulate_off_banner(copies):
        # Helper function to repeatedly simulate pulling the specified
        # copies of the target off banner 4* and return a list to be
        # passed to print_percentiles().
        running_total_pulls = []
        for run in range(100000):
            running_total_pulls.append(run_till_off_banner_4star(copies))
        return running_total_pulls
    
    print("E0 ON")
    print_percentiles(simulate_on_banner(1))
    print()

    print("E1 ON")
    print_percentiles(simulate_on_banner(2))
    print()

    print("E2 ON")
    print_percentiles(simulate_on_banner(3))
    print()

    print("E3 ON")
    print_percentiles(simulate_on_banner(4))
    print()

    print("E4 ON")
    print_percentiles(simulate_on_banner(5))
    print()

    print("E5 ON")
    print_percentiles(simulate_on_banner(6))
    print()

    print("E6 ON")
    print_percentiles(simulate_on_banner(7))
    print()

    print("E0 OFF")
    print_percentiles(simulate_off_banner(1))
    print()

    print("E1 OFF")
    print_percentiles(simulate_off_banner(2))
    print()

    print("E2 OFF")
    print_percentiles(simulate_off_banner(3))
    print()

    print("E3 OFF")
    print_percentiles(simulate_off_banner(4))
    print()

    print("E4 OFF")
    print_percentiles(simulate_off_banner(5))
    print()

    print("E5 OFF")
    print_percentiles(simulate_off_banner(6))
    print()

    print("E6 OFF")
    print_percentiles(simulate_off_banner(7))
    print()


if __name__ == "__main__":
    main()
