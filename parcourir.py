import os, sys, json #importing the necessary tools
from compare import compare #compare is in another script so we also need to import this


# the first script is there to fetch the type of files wanted
# it explore the directory given as path and the directories below that
def cherche_fichier(repertoire,type):
    liste=[] #initiliaze the list which will store those files
    element = os.listdir(repertoire) #list everything in the given path
    #now depending on if this is a directory or a file it will read it's content
    # extract the type and store it or 
    for fichier in element :
        if os.path.isdir(repertoire+"/"+fichier):
            souselement = os.listdir(repertoire+"/"+fichier) 
            for sousfichier in souselement:
                if sousfichier.split(".")[-1]==type:
                    liste.append(repertoire+"/"+fichier+"/"+sousfichier)
        else:
            if fichier.split(".")[-1]=="vcf":
                liste.append(repertoire+"/"+fichier)
    liste.sort()
    return liste

#using the script upward we search for the vcf files
VCF=cherche_fichier(sys.argv[1],"vcf")
#if the list is empty, the script is stopped
if len(VCF)==0 :
    print("no vcf files available")
    sys.exit()

#This script is to sort the content of the list
#and arrange it by specimen through a dicttionnary(dict.)
def trier_echantillon(liste):
    dico_echantillons={}
    for path in liste :
        echantillon=path.split("/")[-1]
        if echantillon[:3] in dico_echantillons :
            dico_echantillons[echantillon[:3]].append(path)
        else:
            dico_echantillons[echantillon[:3]]=[path]
    return dico_echantillons

dico_echantillons=trier_echantillon(VCF)

saisie=input("What range of nucleotides do you want to cover for the comparison ? \n This value is used to compensate alteration like deletion or insertion \n Press enter for default (10)")
if saisie.isdigit():
    range_nucleotides=int(saisie)
else:
    range_nucleotides=10

saisie=input("What ratio of similarity do you want in percent ? \n This value is used as a comparison threshold of meaning what is above this threshold is considered the same \n Press enter for default (75%)")
if saisie.isdigit() and 0<int(saisie)<100:
    ratio_correspondance=int(saisie)/100
else:
    ratio_correspondance=0.75

print(f"Value chosen range of comparison={range_nucleotides} and ratio of comparison={ratio_correspondance*100}%")
print("processing...")
#using the compare script to extract the data of the vcf files
dico_sequence, dico_comparaison=compare(dico_echantillons,range_nucleotides,ratio_correspondance)# put each dictionnary into a variable

#The last part will create a file by specimen to store the said results
#the result can be stored as a txt or a json
type_input=input("\rChoose a type of file to store your results?\n" '''"json" or "txt" ? ''')

#handling exceptions
while (not(type_input=="json" or type_input=="txt")):
    print("Wrong input!")
    type_input=input('''Choose a type of file to store your results? "json" or "txt" ? beware of capital letter ''')


#function to store the created results
def create_results(dico_sequence,dico_comparaison,type):
    header_compare="Percent of similarity between two sample \n"    #header for the compare dictionnary(aka comparison between all replicates)
    header_sequence="\nReplicats | position | Nucleotides or mutation | nb of times it appears\n" #header for the results of each file
    if not os.path.exists("./result"): #create a directory for the results if it's not already there
        os.makedirs("./result")
        print("directory created")
    for echantillons in dico_sequence: # for each sample it will create a new file (if it already exist it will replace it)
        with open(f"./result/{echantillons}.{type}",'w') as file:
            file.write(str(header_compare))   #starting with the header of the comparison
            if(type=="json"): #json file can use an indentation for the results
                json.dump(dico_comparaison[echantillons],file) #write the comparison dictionnary (json.dump is to write a dictionnary making it readable (even if it has no use for this dict.))
                file.write(str(header_sequence)) # then the header of the sequencing
                json.dump(dico_sequence[echantillons],file, indent=4) #writing the dictionnary of the sequencing 
            elif(type=="txt"): # same thing as json but without indent
                file.write(str(dico_comparaison[echantillons]))
                file.write(str(header_sequence))
                file.write(str(dico_sequence[echantillons]))
        print("result file created")

create_results(dico_sequence,dico_comparaison,type_input) #invoke the function with the desired type of file and the 2 dict.
print("files can be found at ./result")