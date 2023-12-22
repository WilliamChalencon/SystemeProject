# SystemeProject
This little script has been made to compare vcf files of multiple biological sample.
It can compare multiple replicates of a sample between them.

It will ask a directory which contains the sample and retrieve all vcf files on 2 levels.
If you have multiple sample, it will sort them out by sample but their name needs to be in this kind of format : {3 character for sample name - 1 character for replicate} ex: P15-2

Once every files is retrieved, it will read them and fetch each sequence and compare it with the others replicates of the same sample.

It will ask a degree of correspondance and a range of nucleotides to compare the sequence.

If two sequence correpond a count will be added to mark how many times a certain sequence have been found.

The script will ask you to store the result in a file txt or json. One file by sample.

The result will be as follows :

header of comparison:
{pair of replicates: percent of similarity,...}

header 
{replicates name : [{position:[nucleotide or mutation, nb of appearance],...},..]}

This script was made by William CHALENCON student at the university of montpellier. An AI was used to help on debugging.
