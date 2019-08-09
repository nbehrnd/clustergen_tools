# name:   cif2clustergen.py
# author: nbehrnd@yahoo.com
# date:   2019-07-30 (YYYY-MM-DD)
# edit:   2019-08-09 (YYYY-MM-DD)
""" provide CLUSTERGEN suitable .inp from .cif read

Run this script -- which must reside in the same folder containing the
.cif to work with -- with the terminal of python3.  (Python2 is not
targeted here.)  Do not provide additional parameters:

    python3 cif2clustergen.py

to obtain one CLUSTERGEN suitable .inp per .cif read.  It does not
moderate the sequential run / dimer identification with CLUSTERGEN, which
is topic of 'serial_clustergen.py'.

Known to work with .cif by i) CCDC CSD database obtained via conquest,
and ii) .cif written by CCDC Mercury3.9; both if these contain only one
model per file.  On the contrary, default formatted .cif provided by
Olex2 (test with release 1.2.10) contain additional columns in the atom
block; such .cif do not work with this script (however, Olex2's .cif pass
the GUI of CLUSTERGEN).

(c) Norwid Behrnd, 2019, GPLv3. """
import fnmatch
import os
import shutil
import sys

# pattern basically copy-pasted from the .inp set to suitable parameters 
global frame
frame = str("""
CLUS 1
!-----
FRGM 1 1 1
!-----
TEST 0
!-----
XYZF 1
!-----
VERB 0
!-----
CHRG 0
!-----
ADFF 0
!-----
SHLX 0
!-----
CRYF 0
!-----
GAUF 0
!-----
DIMR 1
!-----
DMAX 10.0
!-----
TOLS 0.05 0.1 0.08 0.2
!-----
! provision of the lattice constants, start:
CELL 4.6858 8.2573 17.627 90.0 90.0 90.0
! provision of the lattice constants, end.
!-----
GECR 0
!-----
! provision of the symmetry operators' number and format (one line)
! followed by the symmetry operators (contrary to CCDC CSD .cif
! format, this is unnumbered).  Trailing 2 indicates the cif format.
! SYMM 4 2 ! example for four entries provided in the .cif format.
x,y,z
1/2-x,-y,1/2+z
-x,1/2+y,1/2-z
1/2+x,1/2-y,-z
! provision about unit cell symmetry operators, end.
!-----
STXH 0 0
!-----
EXBD 0 0
!-----
! provision of the total number of atoms in all fragments per asym. unit
! provision of fragment 1 and its number of atoms to consider
! each atom's entry (element, label, (x,y,z) tuple -- no e.s.d or blanks
! NFRG 18 1  ! i.e., 18 atoms spread over in total 1 fragment
! FRAG 1 18  ! example about 18 atoms within fragment 1.
N N1 0.6664 0.7427 0.06152
H H1 0.613 0.834 0.0921
H H2 0.811 0.754 0.0362
C C1 0.4417 0.2815 0.13043
C C2 0.3193 0.4148 0.16499
C C3 0.3904 0.5696 0.14419
H H3 0.3044 0.6604 0.1681
C C4 0.5946 0.5901 0.0864
C C5 0.7184 0.4539 0.05165
H H4 0.8549 0.4688 0.0124
C C6 0.6456 0.2999 0.07331
H H5 0.7316 0.2082 0.0501
C C7 0.3209 0.1354 0.16375
O O1 0.3676 -0.00598 0.1503
O O2 0.1279 0.1792 0.21724
C C8 0.1132 0.3541 0.22369
H H6 0.1705 0.39 0.2751
H H7 -0.0823 0.3936 0.2132
! provisions of atoms, end.
!-----
""")


def learn_cif():
    """ identify the .cif to work with """
    global cif_register
    cif_register = []
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "*.cif"):
            cif_register.append(file)
    cif_register.sort()


def write_inp():
    """ discern .cif type, write suitable .inp """
    for entry in cif_register:
        print("Work on {}.".format(entry))
        inp_register = []
        inp_file = str(entry)[:-4] + str(".inp")

        frame_register = []
        counter = 0
        for line in frame.split("\n"):
            # retain = str("{}, {} \n".format(counter, str(line)))
            retain = str("{} \n".format(str(line)))
            frame_register.append(retain)
            counter += 1

        # collection lattice constants
        entry_register = []
        with open(entry, mode="r") as sourcefile:
            for line in sourcefile:
                entry_register.append(str(line).strip())

            lattice_constants = str("CELL ")
            a = b = c = alpha = beta = gamma = ""
            for line in entry_register:
                if str(line).startswith("_cell_length_a"):
                    a = ""
                    for char in line.split()[1]:
                        if str(char) != str("("):
                            a += str(char)
                        else:
                            break

                if str(line).startswith("_cell_length_b"):
                    b = ""
                    for char in line.split()[1]:
                        if str(char) != str("("):
                            b += str(char)
                        else:
                            break

                if str(line).startswith("_cell_length_c"):
                    c = ""
                    for char in line.split()[1]:
                        if str(char) != str("("):
                            c += str(char)
                        else:
                            break

                if str(line).startswith("_cell_angle_alpha"):
                    alpha = ""
                    for char in line.split()[1]:
                        if str(char) != str("("):
                            alpha += str(char)
                        else:
                            break

                if str(line).startswith("_cell_angle_beta"):
                    beta = ""
                    for char in line.split()[1]:
                        if str(char) != str("("):
                            beta += str(char)
                        else:
                            break

                if str(line).startswith("_cell_angle_gamma"):
                    gamma = ""
                    for char in line.split()[1]:
                        if str(char) != str("("):
                            gamma += str(char)
                        else:
                            break

            lattice_constants = ("CELL {} {} {} {} {} {} \n".format(
                a, b, c, alpha, beta, gamma))

            # determine last line prior to the symmetry positions:
            line_prior_positions = entry_register.index(
                "_symmetry_equiv_pos_as_xyz")
            # print("line_prior_positions {}".format(line_prior_positions))
            symmetry_register = []

            # collecting the symmetry information:
            for line in entry_register[line_prior_positions:]:
                if str(line).startswith("_cell_length_a"):
                    break
                if len(str(line)) == 0:
                    break
                if str(line).startswith("loop_"):
                    break
                else:
                    retain = str(line).split()[1:]

                    symmetry_register.append(retain)
            del symmetry_register[0]

            symmetry_entry_kept = str("\nSYMM {} 2 \n".format(
                len(symmetry_register)))

            symmetry_entries = ""
            for entry in symmetry_register:
                retain = str("{} \n".format(str(entry)[2:-2]))
                symmetry_entries += str(retain)

            # collecting information about fractional atomic coordinates:
            # identification last line prior atom block:
            line_prior_coordinates = entry_register.index("_atom_site_fract_z")
            # print("line_prior_coordinates {}".format(
            # line_prior_coordinates +1))
            atom_register = []

            for line in entry_register[(line_prior_coordinates + 1):]:
                if len(str(line).split()) != 5:
                    break
                if len(str(line).split()) == 5:
                    fract_x = ""
                    for char in str(line).split()[2]:
                        if str(char) != str("("):
                            fract_x += str(char)
                        else:
                            break

                    fract_y = ""
                    for char in str(line).split()[3]:
                        if str(char) != str("("):
                            fract_y += str(char)
                        else:
                            break

                    fract_z = ""
                    for char in str(line).split()[4]:
                        if str(char) != str("("):
                            fract_z += str(char)
                        else:
                            break

                    # reorder columns of .cif for CLUSTERGEN / in .inp:
                    retain = str("{} {} {} {} {} \n".format(
                        str(line).split()[1],
                        str(line).split()[0], fract_x, fract_y, fract_z))

                    atom_register.append(retain)

            atom_header = ""
            atom_header += str("NFRG {} 1\n".format(len(atom_register)))
            atom_header += str("FRAG 1 {}\n".format(len(atom_register)))

        # provision first constant block of .inp content
        for entry in frame_register[1:28]:
            inp_register.append(entry)

        # provision of the changing lattice constants
        inp_register.append(lattice_constants)

        # continuation of the constant input
        for entry in frame_register[29:36]:
            inp_register.append(entry)

        # provision of the number of symmetry operators read-out
        inp_register.append(symmetry_entry_kept)
        # followed without break nor blank line about the symmetry
        # operators (second parameter = 2 means in .cif format)
        for entry in symmetry_register:
            retain = str(entry)[2:-2] + str("\n")
            inp_register.append(retain)

        # continuation of the constant input
        for entry in frame_register[40:51]:
            inp_register.append(entry)

        # provision about the atom header
        inp_register.append(atom_header)

        # directly followed by the fractional atomic coordinates in a
        # format different to the in CCDC's .cif
        for entry in atom_register:
            retain = str(entry) + str("\n")
            inp_register.append(entry)

        # continuation of the constant input
        for entry in frame_register[69:]:
            inp_register.append(entry)

        # provide permanent .inp file
        with open(inp_file, mode="w") as newfile:
            for entry in inp_register:
                retain = str(entry)
                newfile.write(retain)


def space_cleaning():
    """ stash originally accessed .cif into a deposit """
    try:
        os.mkdir("cif_deposit_cif2clustergen")
    except:
        pass
    for entry in cif_register:
        try:
            shutil.move(entry, "cif_deposit_cif2clustergen")
        except:
            pass


# action calls:
print("\nScript 'cif2clustergen.py' was started.\n")
learn_cif()
write_inp()

space_cleaning()
print("\nScript 'cif2clustergen.py' closes now.\n")
sys.exit(0)
