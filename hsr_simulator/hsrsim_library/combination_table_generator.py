"""This script is used to generate percentile tables illustrating the
number of pulls that would be needed to reach a certain "level" of a 
character and their signature light cone in Honkai Star Rail. Tables
are generated for the following "levels":

E0, E1, E2, E3, E4, E5, E6, S1, S2, S3, S4, S5, S6, E0S1, E0S2, E0S3, 
E0S4, E0S5, E1S1, E1S2, E1S3, E1S4, E1S5, E2S1, E2S2, E2S3, E2S4, E2S5,
E3S1, E3S2, E3S3, E3S4, E3S5, E4S1, E4S2, E4S3, E4S4, E4S5, E5S1, E5S2,
E5S3, E5S4, E5S5, E6S1, E6S2, E6S3, E6S4, E6S5

This script uses the same code and methodology as the main simulator,
but is significantly less flexible and user friendly as all simulation
parameters are hard-coded into the main method. It is included in this
directory to document and publicize how the published tables were
generated.

Please note, this script conducts a significant number of simulations
and takes a signficant amount of time to run. The exact same results
can be obtained for your specific use case using the main simulator.
Running this file is not reccomended for these reasons.
"""
from sim_tools import run_once, print_percentiles


def print_percentiles_for_level(char_copies, cone_copies, multi_run):
    """Print the percentile breakdown of pulls required to obtain the
    number of copies of a featured 5* character and a featured 5* light
    cone.

    Args:
        char_copies (int): The target number of featured 5* characters.
        cone_copies (int): The target number of featured 5* light cones.
        multi_run (int): The number of simulated trials to run.
    """
    running_total_pulls = []

    for run in range(multi_run):
        # Determine pulls needed for target number of character copies.
        char_run_result = run_once("to number", char_copies, 0, 5.1, 0.6, 0, 0,
                                   False, 8, 73, 50.0, 56.4)
        pulls_to_char = char_run_result[0]
        # Determine pulls needed for target number of light cone copies.
        cone_run_result = run_once("to number", cone_copies, 0, 6.6, 0.8, 0, 0,
                                   False, 7, 65, 75.0, 75.0)
        pulls_to_cone = cone_run_result[0]
        # Determine total pulls needed for target level.
        total_pulls = pulls_to_char + pulls_to_cone

        running_total_pulls.append(total_pulls)

    print_percentiles(running_total_pulls)
    print()


def main():
    """Refer to the module docstring for main method documentation.
    """
    multi_run = 100000

    print("E0")
    print_percentiles_for_level(1, 0, multi_run)
    
    print("E1")
    print_percentiles_for_level(2, 0, multi_run)

    print("E2")
    print_percentiles_for_level(3, 0, multi_run)

    print("E3")
    print_percentiles_for_level(4, 0, multi_run)

    print("E4")
    print_percentiles_for_level(5, 0, multi_run)

    print("E5")
    print_percentiles_for_level(6, 0, multi_run)

    print("E6")
    print_percentiles_for_level(7, 0, multi_run)

    print("S1")
    print_percentiles_for_level(0, 1, multi_run)

    print("S2")
    print_percentiles_for_level(0, 2, multi_run)

    print("S3")
    print_percentiles_for_level(0, 3, multi_run)

    print("S4")
    print_percentiles_for_level(0, 4, multi_run)

    print("S5")
    print_percentiles_for_level(0, 5, multi_run)

    print("E0S1")
    print_percentiles_for_level(1, 1, multi_run)

    print("E1S1")
    print_percentiles_for_level(2, 1, multi_run)

    print("E2S1")
    print_percentiles_for_level(3, 1, multi_run)

    print("E3S1")
    print_percentiles_for_level(4, 1, multi_run)

    print("E4S1")
    print_percentiles_for_level(5, 1, multi_run)

    print("E5S1")
    print_percentiles_for_level(6, 1, multi_run)

    print("E6S1")
    print_percentiles_for_level(7, 1, multi_run)

    print("E0S2")
    print_percentiles_for_level(1, 2, multi_run)

    print("E1S2")
    print_percentiles_for_level(2, 2, multi_run)

    print("E2S2")
    print_percentiles_for_level(3, 2, multi_run)

    print("E3S2")
    print_percentiles_for_level(4, 2, multi_run)

    print("E4S2")
    print_percentiles_for_level(5, 2, multi_run)

    print("E5S2")
    print_percentiles_for_level(6, 2, multi_run)

    print("E6S2")
    print_percentiles_for_level(7, 2, multi_run)

    print("E0S3")
    print_percentiles_for_level(1, 3, multi_run)

    print("E1S3")
    print_percentiles_for_level(2, 3, multi_run)

    print("E2S3")
    print_percentiles_for_level(3, 3, multi_run)

    print("E3S3")
    print_percentiles_for_level(4, 3, multi_run)

    print("E4S3")
    print_percentiles_for_level(5, 3, multi_run)

    print("E5S3")
    print_percentiles_for_level(6, 3, multi_run)

    print("E6S3")
    print_percentiles_for_level(7, 3, multi_run)

    print("E0S4")
    print_percentiles_for_level(1, 4, multi_run)

    print("E1S4")
    print_percentiles_for_level(2, 4, multi_run)

    print("E2S4")
    print_percentiles_for_level(3, 4, multi_run)

    print("E3S4")
    print_percentiles_for_level(4, 4, multi_run)

    print("E4S4")
    print_percentiles_for_level(5, 4, multi_run)

    print("E5S4")
    print_percentiles_for_level(6, 4, multi_run)

    print("E6S4")
    print_percentiles_for_level(7, 4, multi_run)

    print("E0S5")
    print_percentiles_for_level(1, 5, multi_run)

    print("E1S5")
    print_percentiles_for_level(2, 5, multi_run)

    print("E2S5")
    print_percentiles_for_level(3, 5, multi_run)

    print("E3S5")
    print_percentiles_for_level(4, 5, multi_run)

    print("E4S5")
    print_percentiles_for_level(5, 5, multi_run)

    print("E5S5")
    print_percentiles_for_level(6, 5, multi_run)

    print("E6S5")
    print_percentiles_for_level(7, 5, multi_run)

if __name__ == "__main__":
    main()