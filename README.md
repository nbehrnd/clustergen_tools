
# Table of Contents

1.  [Background](#org75902d7)
2.  [Use](#org7a0f4fa)


<a id="org75902d7"></a>

# Background

Based on `.cif` files, CLUSTERGEN<sup><a id="fnr.1" class="footref" href="#fn.1">1</a></sup> provides facilitates to
identify and write `.xyz` files about dimers and clusters suitable
for further analysis and quantum chemical computation.  It equally
offers the direct output in formats suitable for ADF and Gaussian.

To automate the identification of "interesting dimers", `.cif` model
data may be converted batch-wise into intermediate `.inp` input files
suitable for a sequential processing with CLUSTERGEN's `.f90` source
code.  Similarly, it is possible to systematically build clusters.
Three complementary definitions regarding the distance threshold of
inner (reference) molecule and most outer neighbor are available.


<a id="org7a0f4fa"></a>

# Use

Put the `.cif` of interest, the `.f90` source code of CLUSTERGEN
(available from the author) and the two scripts into the same
folder.  A call of

    python cif2clustergen.py

creates the intermediate `.inp` files.  A subsequent

    python serial_clustergen.py

then both compiles the source-code with `gfortran`, as well provides
the results accessed by `CLUSTERGEN`.


# Footnotes

<sup><a id="fn.1" href="#fnr.1">1</a></sup> "CLUSTERGEN: a program for molecular cluster generation from
crystallographic data", R. Kaminski, K. N. Jarzembska and S. Domagala
in *J. Appl. Cryst.* (2013) ****46****, 540-543,
[doi:10.1107/S0021889813002173](10.1107/S0021889813002173); Windows compiled executable on
[http://www.photocrystallography.eu/software.html](http://www.photocrystallography.eu/software.html).
