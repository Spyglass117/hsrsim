This repository contains a simple Python script for simulating large quantities of Gacha draws/pulls across multiple trials. 
The intended usage is for generating, visualizing, and analyzing a population of Gacha draw results by using a bootstrap-like
approach to simulate many psuedo-random artificial samples. The script is equipped with two sampling modes, and is able to
calculate and output descriptive statistics and frequency histograms to describe the generated population. A user familiar
with using Python for modeling or statistical purposes can add additional code as they wish to conduct statistical tests or
generate plots not included in the program by default.

Percentile data generated by this simulator can be found here: 
https://docs.google.com/spreadsheets/d/e/2PACX-1vQBKYotQAAKYHK42y2QQDvHIJ7echx4Lqp6J2vRghrybtH55BbNV9b7GC1vI--fTp4GJsulcxwXEwE1/pubhtml

To use this simulator, you will need Python > 3.10 installed locally on your system. I recommend Miniconda (which can be
downloaded here: https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/) paired with Visual Studio Code,
a free, lightweight code editor developed by Microsoft available through the Microsoft store or online 
(https://code.visualstudio.com/). If you install Miniconda with the reccomended settings, VSCode should automatically
detect the Python interpreter installed with Miniconda, but if it does not use Ctrl + Shift + P and click "Select Python
Interpreter." The code in this repository requires the 'math', 'matplotlib', 'numpy', and 'random' modules to be installed in the
Python environment you intend to run the code in. 'math' and 'random' should be installed by default, but before running the
program, you will need to open the Anaconda Powershell Prompt application installed with Miniconda and type "conda install numpy"
and "conda install matplotlib". If you encounter any issues, there are plenty of getting started with Python resources available
online; any method of installing Python will work as long as you have an up to date version and the required modules. The whole
process should only take a few minutes, but if you're really struggling, shoot me a message on Reddit and I'll do my best to help
you troubleshoot.

If you don't want to bother setting up a local python environment, you may be able to find an online interpreter to run this code in.
You will need to copy and past the contents of the sim_calculators.py and sim_tools.py folders directly above line 195 in main.py and
delete the import statements that reference those folders at the top of that file, then copy and paste the code into your interpreter of
choice. In my limited testing, I have found that many online interpreters struggle with the numpy dependency, but if you find one that
works please let me know.

Development of this simulator and the subsequent data compilation and reporting was extremely time consuming. Please consider supporting
me using the Ko-Fi link on this page.
