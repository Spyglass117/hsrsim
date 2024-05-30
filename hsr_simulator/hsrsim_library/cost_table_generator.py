"""Simple script for generating a cost table from 10 up to 2000 pulls.
"""
import csv
from sim_calculators import costs


def main():
    """Write the jade and dollar costs from 10 to 2000 pulls in
    increments of 10 to a CSV file.

    Each row contains the jade cost, least expensive dollar cost,
    least expensive dollar cost considering the first top up bonus,
    most efficient dollar cost, and most efficient dollar cost
    considering the first top up bonus.
    """
    with open('cost_table.csv', 'w', newline = '') as out_file:
        csvwriter = csv.writer(out_file)
        for pulls in range(10, 2001, 10):
            csvwriter.writerow(costs(pulls))


if __name__ == "__main__":
    main()