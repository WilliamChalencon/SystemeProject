import os, sys, json # importing the necessary tools
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
#and arrange it by specimen through a dict
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

#using the compare script to extract the data of the vcf files
resultats=compare(dico_echantillons)

#The last part will create a file by specimen to store the said results
#the result can be stored as a txt or a json
type_input=input('''Choose a type of file to store your results? "json" or "txt" ? ''')

#handling exceptions
while (not(type_input=="json" or type_input=="txt")):
    print("Wrong input!")
    type_input=input('''Choose a type of file to store your results? "json" or "txt" ? beware of capital letter ''')

def create_results(dico_echantillons,type):
    if not os.path.exists("./result"):
        os.makedirs(".result")
        print("directory created")
    for echantillons in dico_echantillons:
        with open(f"./result/{echantillons}.{type}",'w') as file:
            if(type=="json"):
                json.dump(dico_echantillons[echantillons],file, indent=4)
            elif(type=="txt"):
                file.write(str(dico_echantillons[echantillons]))
        print("result file created")

create_results(resultats,type_input)
print("files can be found at ./result")