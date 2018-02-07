# Deduper

The contents of this repo is part of a class assignment. The code can be found in `part3/`.

A script to remove PCR duplicates from a SAM file of uniquely mapped reads. The script will retain only a single copy of each read and outputs the first read encountered if duplicates are found. The output file will have "_deduped" attached to the input file name. Currently ONLY SINGLE-END SAM files can be passed into the script. If UMIs were used in sequencing, a file of the used UMIs can be passed, else randomers will be used. Last updated: January 11, 2017.


### Part 3

Please look at the part3/ folder for the deduper code

### Part 1
Write up a strategy for writing a Reference based PCR duplicate removal tool. Be sure to include an example input and output SAM file.

strategy & pseudo-code are in the files starting with "ho_de_duper_1" (different extensions)

example SAM files are in SAM_files/

misc_notes/ notes, etc. currently has the psuedo-code (.txt)
