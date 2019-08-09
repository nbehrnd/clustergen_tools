# name:   serial_clustergen.py
# author: nbehrnd@yahoo.com
# date:   2019-08-02 (YYYY-MM-DD)
# edit:   2019-08-09 (YYYY-MM-DD)
""" moderate CLUSTERGEN with Python to work batchwise

The .inp instruction files provided by cif2clustergen.py for CLUSTERGEN
are processed sequentially with this moderator script.  Deposit this
script into the same folder as the .inp as well as the .f90 source code
of CLUSTERGEN.  Launch the execution of this script from the CLI by

python3 serial_clustergen.py

without the provision of any parameter.  Targeted platform is Python3 in
Linux Xubuntu 18.04.2 / Debian 10 buster; apparently equally working with
Python2.7.15+, though.  The callable presence of gfortran7 or gfortran8
to compile an executable of CLUSTERGEN is a mandatory requirement.
(c) Norwid Behrnd, 2019, GPLv3. """

import fnmatch
import os
import shutil
import subprocess as sub
import sys

global inp_register
inp_register = []


def learn_inp():
    """ identify the .inp eventually to relay to CLUSTERGEN """
    print("Identification of .inp files started.")
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "*.inp"):
            inp_register.append(file)
    inp_register.sort()
    print("Identification of .inp files completed.\n")


def compile_f90():
    """ compile the complete array of Fortran .f90 source """
    print("Compilation of the .f90 source code started.")
    command_compile = str("gfortran -O3 -o clustergen *.f90")
    sub.call(command_compile, shell=True)
    print("Compilation of the .f90 source code completed.\n")


def search_dimers():
    """ moderate CLUSTERGEN to identify the dimers """
    print("Relayed identification of dimers started.")
    for entry in inp_register:
        print("\nWork on {}.".format(entry))

        command = str("./clustergen {}".format(entry))
        sub.call(command, shell=True)

        # space cleaning:
        model_deposit = str(entry)[:-4]
        try:
            os.mkdir(model_deposit)
        except OSError:
            pass

        try:
            shutil.move(entry, model_deposit)
            out_file = str(entry)[:-4] + str(".out")
            shutil.move(out_file, model_deposit)
        except OSError:
            pass

        # first rename the dimer .xyz, than equally deposit them
        for file in os.listdir("."):
            if fnmatch.fnmatch(file, "*.xyz"):
                old_name = str(file)
                new_name = str(model_deposit) + str("_") + str(file)
                shutil.move(old_name, new_name)

                shutil.move(new_name, model_deposit)

    print("Identification of dimers complete.\n")


# action calls:
print("Script 'serial_CLUSTERGEN.py' started.\n")
learn_inp()
compile_f90()

search_dimers()
print("\nScript 'serial_CLUSTERGEN.py' closes.\n")
sys.exit(0)
