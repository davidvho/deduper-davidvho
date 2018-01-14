ho_deduper.py

A script to remove PCR duplicates from a SAM file of uniquely mapped reads. The script will retain only a single copy of each read and outputs the first read encountered if duplicates are found. The output file will have "_deduped" attached to the input file name. Currently ONLY SINGLE-END SAM files can be passed into the script. If UMIs were used in sequencing, a file of the used UMIs can be passed, else randomers will be used. Last updated: January 11, 2017.

----

Results from the files on Talapas when ran locally on my computer and the run times, using the list of UMIs provided:

Dataset 1:

Alignments before deduping: 1013180
Alignments after deduping: 635985
Number of duplicates removed: 377195
UMI list was supplied. Alignments with bad UMIs: 8190

real	3m7.513s
user	2m10.507s
sys	0m40.816s


Dataset 2:

Alignments before deduping: 1382109
Alignments after deduping: 744188
Number of duplicates removed: 637921
UMI list was supplied. Alignments with bad UMIs: 9319

real	3m46.760s
user	2m48.817s
sys	0m48.821s


Dataset 3:

Alignments before deduping: 5721150
Alignments after deduping: 4053643
Number of duplicates removed: 1667507
UMI list was supplied. Alignments with bad UMIs: 48939

real	19m22.825s
user	13m6.012s
sys	4m23.156s
