import sys,os

#this script is to see if two sequence correspond with each other
#it will return a ratio of corresponding nucleotides
def Comparaison(sequence1,sequence2):
    correspondance=0.0
    for i in range(len(sequence1)):
        if sequence1[i]==sequence2[i]:
            correspondance +=1.0
    correspondance=correspondance/len(sequence1)
    return correspondance

#This function is for reading the files, fetching each read with it's position,
def compare(dico,range_nucleotides,ratio_correspondance):
    dico_echantillons = {} #one dict to store each specimen
    dico_compare= {} #one dict to compare each specimen comparison
    exception = ['<DUP>', '<INS>', '<DEL>'] # the kind of exception we encounter
    for echantillons in dico: #going through each specimene
        dico_replicats = {}#one dict for each sample of specimen
        dico_compare_replicats={}#one dict to compare each replicats of specimen
        for replicats in dico[echantillons]: #going through each replicats
            nom_fichier_replicats = (replicats.split("/")[-1]) #take the file name
            nom_replicats=nom_fichier_replicats[:5] #to extract the replicats name
            replicat_variants = [] #create a list with each read
            file = open(replicats, 'r') #open the file
            i = 0 #create a count to count lines 
            sequençage = {}
            
            for line in file:
                correspondance = False #variable to know if it's a new sequence or not
                i += 1
                if i > 49: #skip the header 
                    position = int(line.split('\t')[1])
                    #this part will compare the read line with the sequence already registered
                    for compare_replicats in dico_replicats: #going throught all the dict.
                        if nom_replicats != compare_replicats:# don't compare it with the same replicate
                            for compare_sequence in dico_replicats[compare_replicats]:
                                if isinstance(compare_sequence,dict):
                                    while not correspondance :
                                        #there is a comparaison for every sequence in a range +/-10 position
                                        for compare_position in range(position - range_nucleotides, position + range_nucleotides): #use only the position within range
                                            if compare_position in compare_sequence: #verify if the position exist
                                                try:
                                                    sequence1 = [char for char in line.split('\t')[4]] # put the read in a list to compare it with other sequence already registered
                                                    for position_sequence2 in range(compare_position - range_nucleotides,compare_position + range_nucleotides): 
                                                        sequence2 = [] #initialize a list of another sequence to compare
                                                        for nombre_nucleotides in range(len(sequence1)): #create the list with the nucleotides 
                                                            liste_position = compare_sequence[position_sequence2 + nombre_nucleotides]
                                                            sequence2.append(liste_position[0])

                                                        if Comparaison(sequence1, sequence2) > ratio_correspondance: #if correspondance is supperior to the defined ratio
                                                            correspondance = True
                                                            key=f"{compare_replicats} with {nom_replicats}" #name the pair of replicates with the correpondant sequence
                                                            if key in dico_compare_replicats: 
                                                                dico_compare_replicats[key]=dico_compare_replicats[key]+1#add a count to a dictionnary
                                                            else:
                                                                dico_compare_replicats[key]=1#create one entry if it's not registered
                                                            for nombre_nucleotides in range(len(sequence1)): # for each position add a +1 to each nucleotides increasing the count
                                                                liste_position = compare_sequence[position_sequence2 + nombre_nucleotides]
                                                                liste_position[1] = liste_position[1] + 1
                                                                compare_sequence[position_sequence2 + nombre_nucleotides] = liste_position
                                                                dico_replicats[compare_replicats] = compare_sequence
                                                            break
                                                except KeyError : # if the position is not in the dictionnary skip to get to try another one 
                                                    continue
                                        break
                    # if there is no correspondance this will add the sequence in the dictionnary
                    if not correspondance: #if there is no correspondance found add the sequence with each position in the dictionnary
                        if line.split('\t')[4] in exception: # if it is a mutation then the whole segment is added
                            compteur = [line.split('\t')[4], 1] # list with mutation and nb of nucleotides
                            sequençage[position]=compteur
                        else:
                            for nucleotides in line.split('\t')[4]: #if it is a sequence then it's added one nucleotides at a time 
                                compteur = [nucleotides, 1] 
                                sequençage[position]=compteur
                                position += 1 #increment the position
                
            replicat_variants.append(sequençage) #add the sequence to the list
            dico_replicats[nom_replicats] = replicat_variants #add it to the dict
                
            for paire_replicats in dico_compare_replicats: #make a percent value if the it found correspondant
                if replicats in paire_replicats:
                    dico_compare_replicats[paire_replicats]=(dico_compare_replicats[paire_replicats]/(i-49))*100
                     
            dico_compare[echantillons]=dico_compare_replicats  #put the dictionnary of replicates comparison in the compare dict      
            dico_echantillons[echantillons] = dico_replicats #put the dict of replicates in the dictionnary of sample

    return dico_echantillons,dico_compare #return both dictionnary
