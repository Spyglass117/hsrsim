This repository contains a simple Python script for simulating large quantities of Gacha draws/pulls across multiple trials. 
The intended usage is for generating, visualizing, and analyzing a population of Gacha draw results by using a bootstrap-like
approach to simulate many psuedo-random artificial samples. The script is equipped with two sampling modes, and is able to
calculate and output descriptive statistics and frequency histograms to describe the generated population. A user familiar
with using Python for modeling or statistical purposes can add additional code as they wish to conduct statistical tests or
generate plots not included in the program by default.

The script is intended to be edited directly by the user, and does not feature any form of user or application interface
whatsoever. Also, because of several... "sub-optimal" design decisions made for the sake of development efficiency, several
components of this script can not effectively be used if imported into another module.

Therefore it is reccomended to either download the file "main.py" and open it locally, or import the code in "main.py" into
an online interpreter such as runpython.org and run it there. If you know nothing about Python, using an online interpreter
is the reccomended approach. Simply import the code, and follow the directions in the file for modifying the simulation
parameters, then run the file to print the output.

If you choose to run the script locally, be advised that it was developed on Python 3.12.3 and requires the random,
numpy, and matplotlib modules to be installed in your Python environment. Be aware that the script may not work properly
on Python versions prior to 3.10 as some functionality relies on Match Case statements. If you are hellbent on running it
on an earlier version of Python, you are welcome to dig out those statements and replace them with if blocks provided you
don't try and go back past 3.6 as F strings are used in essentially all output formatting. If you don't know what any of
that means, are just here to simulate your own pulls, and/or do not want to bother setting up your own Python environment,
go back to line 11.

Documentation for the code itself is provided in "main.py" and you can go read it there if you're a nerd.
