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
def compare(dico):
    dico_echantillons = {} #one dict to store each specimen
    exception = ['<DUP>', '<INS>', '<DEL>'] # the kind of exception we encounter
    for echantillons in dico:
        dico_replicats = {}#one dict for each sample of specimen

        for replicats in dico[echantillons]:
            replicat_variants = []
            file = open(replicats, 'r')
            i = 0
            sequençage = {}

            for line in file:
                correspondance = False
                i += 1
                    #faire un cas des exceptions
                if i > 49: #skip the header 
                    position = int(line.split('\t')[1])
                    #this part will compare the read line with the sequence already registered
                    for compare_replicats in dico_replicats:
                        for compare_sequence in dico_replicats[compare_replicats]:
                            if isinstance(compare_sequence,dict):
                                while not correspondance :
                                    #there is a comparaison for every sequence in a range +/-10 position
                                    for compare_position in range(position - 10, position + 10):
                                        if compare_position in compare_sequence:
                                            try:
                                                sequence1 = [char for char in line.split('\t')[4]]
                                                for position_sequence2 in range(compare_position - 10,compare_position + 10): #mettre en arguments
                                                    sequence2 = []
                                                    for nombre_nucleotides in range(len(sequence1)):
                                                        liste_position = compare_sequence[position_sequence2 + nombre_nucleotides]
                                                        sequence2.append(liste_position[0])

                                                    if Comparaison(sequence1, sequence2) < 0.75: # mettre en arguments
                                                        correspondance = True

                                                        for nombre_nucleotides in range(len(sequence1)):
                                                            liste_position = compare_sequence[position_sequence2 + nombre_nucleotides]
                                                            liste_position[1] = liste_position[1] + 1
                                                            compare_sequence[position_sequence2 + nombre_nucleotides] = liste_position
                                                            dico_replicats[compare_replicats] = compare_sequence
                                                        break
                                            except KeyError :
                                                continue
                                    break
                    # if there is no correspondance this will add the sequence in the dictionnary
                    if not correspondance:
                        if line.split('\t')[4] in exception:
                            compteur = [line.split('\t')[4], 1]
                            sequençage[position]=compteur
                        else:
                            for nucleotides in line.split('\t')[4]:
                                compteur = [nucleotides, 1]
                                sequençage[position]=compteur
                                position += 1

                replicat_variants.append(sequençage)
                nom_replicats = (replicats.split("/")[-1])
                dico_replicats[nom_replicats[:5]] = replicat_variants

            dico_echantillons[echantillons] = dico_replicats

    return dico_echantillons
    
#nombre de correspondance pour chaque paire de replicats
