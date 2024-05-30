"""Contains functions for calculating the dollar cost and stardust
gained from a number of pulls in Honkai Star Rail.
"""
import random


def dollar_cost(pulls, double_top_up = False, e_mode = False):
    """Return the number of dollars needed for the specified pulls.
    
    This function attempts to approximate the dollar cost of buying the
    specified number of pulls. If the first top up bonus is available,
    the function first tries to reach the target number of stellar jade
    by purchasing only packages with a bonus, from least expensive to
    most expensive. After all first top up bonuses are depleted, or if 
    double_top_up is initially set to false, the function will purchase
    oneiric shards at the regular price.

    Args:
        pulls (int): The number of pulls to approximate the cost for.
        double_top_up (bool): Whether the first purchase bonus is
            available. Defaults to False.
        e_mode (bool): If False, attempts to minimize the dollar cost of
            purchased jade even if doing so would be less efficient than
            purchasing a more expensive package. If True, after using up
            all double top up packcages, only purchases the $99.99
            package. Defaults to False.
        
    Returns:
        [float, int]: [dollar cost of pulls, any leftover jade]
    """
    jade_needed = pulls * 160
    jade_purchased = 0
    cost_of_jade = 0

    # Enough If statements to make YandereDev blush.
    while jade_purchased < jade_needed:
        # Calculate the amount of jade that still needs to be purchased.
        # Used to minimize dollar cost to avoid overbuying jade.
        still_needed = jade_needed - jade_purchased
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
        # If all double bonuses used, continues purchasing normally.
        if jade_purchased < jade_needed and (still_needed >= 7760 or e_mode):
            jade_purchased += 8080
            cost_of_jade += 99.99
            continue
        if jade_purchased < jade_needed and still_needed >= 3734:
            jade_purchased += 3880
            cost_of_jade += 49.99
            continue
        if jade_purchased < jade_needed and still_needed >= 2180:
            jade_purchased += 2240
            cost_of_jade += 29.99
            continue
        if jade_purchased < jade_needed and still_needed >= 990:
            jade_purchased += 1090
            cost_of_jade += 14.99
            continue
        if jade_purchased < jade_needed and still_needed >= 300:
            jade_purchased += 330
            cost_of_jade += 4.99
            continue
        if jade_purchased < jade_needed:
            jade_purchased += 60
            cost_of_jade += 0.99

    leftover_jade = jade_purchased - jade_needed
    # Under esoteric circumstances it is apparently possible to obtain
    # cost estimates with a significantly greater decimal scale than
    # they should have. I've checked and the math is still correct, so
    # for the moment rounding the cost before returning it serves to
    # eliminate the 17 extra decimal places that like popping up.
    cost_of_jade = round(cost_of_jade, 2)
    return [cost_of_jade, leftover_jade]


def costs(pulls):
    """Return a list of jade and dollar costs for the specified pulls.

    Args:
        pulls (int): The number of pulls to output costs for.

    Returns:
        [int, int, float, float, float, float]: [pulls, jade cost, least 
            expensive dollar cost, least expensive dollar cost with top
            up bonus, most efficient dollar cost, most efficient dollar
            cost with top up bonus]
    """
    jade = pulls * 160
    least_expensive = dollar_cost(pulls, False, False)[0]
    least_expensive_double = dollar_cost(pulls, True, False)[0]
    most_efficient = dollar_cost(pulls, False, True)[0]
    most_efficient_double = dollar_cost(pulls, True, True)[0]

    return [pulls, jade, least_expensive, least_expensive_double,
            most_efficient, most_efficient_double]


def estimate_stardust(trial_data, owned_4stars, owned_5stars, e6_4stars,
                      e6_5stars, owned_feat1, owned_feat2, owned_feat3,
                      banner_type = "character"):
    """Estimate stardust gained in a distribution of pulls.

    For each 4* and 5* result in a pull distribution, estimates whether
    the drawn entity is a duplicate based upon the initial number and
    eidolon levels of 4* and 5* entities owned by the user. The trial
    data provided as a parameter to this function must be in the format
    returned by the main.run_once() function.

    Outside of the featured 4* units, eidolon levels are not tracked as
    it is assumed that the chances of repeatedly pulling duplicate, non-
    featured 4* or 5* entities over a relatively small number of pulls
    are negligible. This means that the accuracy of the estimate
    returned by this function will degrade as the number of pulls
    increases.

    Accurately calculating stardust gain would require the user to input
    information on the exact number and eidolon levels of all 4* and
    standard 5* units, and this function would need to assign all draws
    to a specific character and track eidolon levels through execution.
    This is entirely possible, but is too complex for this use case and
    input mode.

    Args:
        trial_data ([int, int, int, int, int, int]): [total pulls,
            number of 3*s, number of non-featured 4*s,
            number of featured 4*s, number of non-featured 5*s, 
            number of featured 5*s]
        owned_4stars (int): The number of 4* entities already owned.
        e6_4stars (int): The number of 4* characters at e6.
        owned_5stars (int): The number of standard banner 5* entities
            already owned.
        e6_5stars (int): The number of standard 5* characters at e6.
        owned_feat1 (int): The number of copies of the first featured 4*
            already owned by the user.
        owned_feat2 (int): The number of copies of the second featured
            4* already owned by the user.
        owned_feat3 (int): The number of copies of the third featured 4*
            already owned by the user.
        banner_type (str): Either "character" or "light cone".

    Returns:
        [int, int, int]: [dust, pulls, remaining dust]
    """
    # Certain loops in this function will not work if the input list
    # contains floats.
    trial_data = [round(x) for x in trial_data]

    # Unpack input data in the same format as output by run_once().
    total_pulls, num_3stars, num_other_4stars, num_featured_4stars, \
        num_other_5stars, num_featured_5stars = trial_data
    
    dust = 0
    # Estimate chances of duplicate based on initial user data.
    dupe_chance_4star = (owned_4stars/21) * 100
    if owned_4stars > 0:
        max_eidolon_chance_4star = (e6_4stars/owned_4stars) * 100
    else:
        max_eidolon_chance_4star = 0
    dupe_chance_5star = (owned_5stars/7) * 100
    if owned_5stars > 0:
        max_eidolon_chance_5star = (e6_5stars/owned_5stars) * 100
    else:
        max_eidolon_chance_5star = 0

    # Calculate duplicates and dust gain for non-featured 4* entities.
    for entity in range(num_other_4stars):
        dupe_roll = random.uniform(0.00001, 100)
        is_character = random.getrandbits(1)
        if dupe_roll <= dupe_chance_4star:
            dust += 8
            if is_character and dupe_roll <= max_eidolon_chance_4star:
                dust += 12
    # Calculate duplicates and dust gain for featured 4* entities.
    if banner_type == "character":
        for entity in range(num_featured_4stars):
            match random.randint(1, 3):
                case 1:
                    owned_feat1 += 1
                    if owned_feat1 == 1:
                        continue
                    elif owned_feat1 <= 7:
                        dust += 8
                    elif owned_feat1 > 7:
                        dust += 20
                case 2:
                    owned_feat2 += 1
                    if owned_feat2 == 1:
                        continue
                    elif owned_feat2 <= 7:
                        dust += 8
                    elif owned_feat2 > 7:
                        dust += 20
                case 3:
                    owned_feat3 += 1
                    if owned_feat3 == 1:
                        continue
                    elif owned_feat3 <= 7:
                        dust += 8
                    elif owned_feat3 > 7:
                        dust += 20
    if banner_type == "light cone":
        # Light cones do not have eidolons and always give 8 stardust.
        dust += num_featured_4stars * 8
    # Calculate duplicates and dust gain for non-featured 5* units.
    for character in range(num_other_5stars):
        dupe_roll = random.uniform(0.00001, 100)
        is_character = random.getrandbits(1)
        if dupe_roll <= dupe_chance_5star:
            dust += 40
            if is_character and dupe_roll <= max_eidolon_chance_5star:
                dust += 60
    # Calculate duplicates and dust gain for featured 5* units.
    if num_featured_5stars > 1 and num_featured_5stars < 8:
        dust += (num_featured_5stars - 1) * 40
    if num_featured_5stars >= 8:
        dust += 240
        dust += (num_featured_5stars - 7) * 100

    pulls = dust // 20
    remaining_dust = dust % 20

    return [dust, pulls, remaining_dust]