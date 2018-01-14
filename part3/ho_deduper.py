#!/usr/bin/env python

##################################
## ARGPARSE ######################
##################################

import argparse

def deduper():
	parser = argparse.ArgumentParser(description='A script to remove PCR duplicates from a SAM file of uniquely mapped reads. The script will retain only a single copy of each read and outputs the first read encountered if duplicates are found. The output file will have "_deduped" attached to the input file name. Currently ONLY SINGLE-END SAM files can be passed into the script. If UMIs were used in sequencing, a file of the used UMIs can be passed, else randomers will be used. Last updated: January 11, 2017.')
	parser.add_argument("-f", "--file", help="Required. Absolute file path to SAM file.", required=True, type=str)
	parser.add_argument("-p", "--paired", help="Optional. Input SAM file is from paired-end data, not single-end --NOT SUPPORTED YET. Default: single-end.", action="store_true", required=False, default=False)
	parser.add_argument('-u','--umi', help='Optional. Absolute path to list of UMIs, one per line. If no UMI list is provided, PCR duplicate removal will be performed based on randomers.', required=False, type=str)
	return parser.parse_args()

args = deduper()

if args.paired:
     raise NameError('Paired-end data is not yet supported. Input SAM file should be single-end at this time.')

# File
file = args.file
umi_input_file = args.umi


########################################
## DEFINITIONS AND FUNCTIONS ###########
########################################

## Strandedness
def bit_checker(line):
    '''Takes the bitwise flag from SAM file and checks it for stranded-ness. Assumes read is mapped and data is single-end. Returns "+" or "-", depending on strand.'''
    
    flag = int(line[1])
    
    #check if read is mapped
    if (flag & 4) == 4:
        
        return None
    
    strand = "+"
    
    if (flag & 16) == 16:      #changes strand if bit 16 is set
        strand = "-"
        
    return strand

## Position and CIGAR string correcting

def position(line):
    '''Looks for the start position in SAM line and corrects if necessary due to CIGAR string (soft-clipping)'''
    
    pos = int(line[3])   # fourth column
    cigar = line[5]   # sixth column
    
    correct_pos = pos
    
    if "S" not in cigar:
        correct_pos = pos
        
    elif cigar.find("S") < cigar.find("M"):
        
        soft_clip = int(cigar.split("S")[0])
        correct_pos = pos - soft_clip
    
#     elif cigar.find("S") > cigar.find("M"):
#         correct_pos = pos

    return correct_pos
   
 
## Chromosome

def chromosome(line):
    '''Looks for the chromosome in a SAM line'''
    
    chrom = line[2]  #third column
    
    return chrom


## UMI in the alignment

def umi_read(line):
    '''Looks for the UMI in the QNAME in a SAM line'''
    
    qname = line[0]
    umi = qname.split(":")[-1]   ## take the last part of the qname, which should be the umi/randomer that was sequenced
    
    return umi


## List of known UMIs

def umi_list(umi_file):
    '''Reads in a txt file where each line is one known UMI to check against'''
    
    umi_dict = {}
    
    for line in open(umi_file):
        umi_dict[line.strip('\n')] = 1
    
    return umi_dict
    
    
##########################
## MAIN ##################
##########################

uniq_align = {}   ## initiate a dictionary to store alignments to check against

align_before = 0    ##count of alignments before deduping
bad_umis = 0     ##count of alignments with 'bad' UMIs

with open(file, "r") as fh:
    
    for line in fh:
        
        if line.startswith('@'):    ## write out the header lines
            with open(file+"_deduped", "a") as myfile:    ## the new file has "_deduped" added to the end
                myfile.write(line)
        
        if not line.startswith('@'):   ## alignment lines
            align_before += 1          ## add to the count
            samline = line.split('\t')    ## split the alignment line into the different parts
            
            if args.umi:   ## if an UMI list is provided,
                umis = umi_list(umi_input_file)   ## create a dictionary using the umi_list function to check alignment umis against
                if umi_read(samline) in umis:    ## if the alignment umi matches the known umi list
                    important_parts = (umi_read(samline), chromosome(samline), position(samline), bit_checker(samline))  ## store the important parts to determine PCR duplicate

                    if important_parts not in uniq_align:   ## if the important parts are not in the uniq_align dict, then it is the first time we encountered this read
                        uniq_align[important_parts] = 1     ## add a count

                        with open(file+"_deduped", "a") as myfile:   ## write out the SAM line
                            myfile.write(line+"\n")
                    else:
                        uniq_align[important_parts] += 1   ## if the important parts are IN the uniq_align dict already, this alignment is a duplicate, add a count only, continue to next line
                else:
                    bad_umis += 1  ## if the alignment umi does NOT match the known umi list, just add a count and the SAM line will not be written out

            else:   ## if an UMI list is NOT provided, use randomers -- as in just look at the alignment randomers and compare against that, no reads will be thrown out due to not matching a known list because there is not list to compare against, so this will not detect sequencing errors
                important_parts = (umi_read(samline), chromosome(samline), position(samline), bit_checker(samline))

                if important_parts not in uniq_align:
                    uniq_align[important_parts] = 1

                    with open(file+"_deduped", "a") as myfile:
                        myfile.write(line+"\n")
                else:
                    uniq_align[important_parts] += 1



print("Done. A SAM file with PCR duplicates removed has been written with '_deduped' attatched to the end of the input SAM file name.")
print()
print("Alignments before deduping:",align_before)
print("Alignments after deduping:",len(uniq_align))
print("Number of duplicates removed:",align_before-len(uniq_align))
if args.umi:  ## if an UMI list was provided, print out how many alignments were thrown out due to not matching the known list
	print("UMI list was supplied. Alignments with bad UMIs:",bad_umis)