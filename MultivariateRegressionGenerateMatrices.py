import os
import pickle as pkl
import numpy as np


home_folder="/home/bsg348/"
bio_unweighted='bio_unweighted_dict.pkl'
bio_weighted='bio_weighted_dict.pkl'
bio_folder="bioaverage/"
similarity_folder="CircuitYearLevel/"

circuit_year=os.listdir(home_folder+bio_folder)
number_of_ckt_years=616
number_of_bio_characteristics=61
number_of_thermometers=40
Z_matrix=np.zeros((number_of_ckt_years*number_of_thermometers,number_of_bio_characteristics))
X_matrix=np.zeros((number_of_ckt_years*number_of_thermometers,number_of_bio_characteristics))
S_matrix=np.zeros((number_of_ckt_years*number_of_thermometers,1))
counter=0
for ckt_yr in circuit_year:
    print(ckt_yr)
    name_file_similarity=home_folder+similarity_folder+ckt_yr+".0.p"
    name_file_bio_weighted=home_folder+bio_folder+ckt_yr+"/"+bio_weighted
    name_file_bio_unweighted=home_folder+bio_folder+ckt_yr+"/"+bio_unweighted
    file_similarity=pkl.load(open(name_file_similarity,'rb'))

    file_bio_weighted=pkl.load(open(name_file_bio_weighted,'rb'))
    #print("abc",file_bio_weighted['x_phouse'])
    file_bio_unweighted = pkl.load(open(name_file_bio_unweighted, 'rb'))
    #print("pqr",file_bio_unweighted['x_phouse'])
    S_matrix[counter:counter+number_of_thermometers]=file_similarity.reshape((number_of_thermometers,1))

    incr=0
    for bio_char in file_bio_weighted.keys():
        #print(bio_char)
        Z_matrix[counter:counter+number_of_thermometers,incr]=file_bio_weighted[bio_char]
        #print("abc",file_bio_weighted[bio_char])
        #print("pqr",file_bio_unweighted[bio_char])
        X_matrix[counter:counter+number_of_thermometers,incr]=file_bio_unweighted[bio_char]
        incr += 1

    counter+=number_of_thermometers

print("dumping Z matrix")
pkl.dump(Z_matrix,open(home_folder+"Z_matrix.pkl","wb"))
print("dumping X matrix")
pkl.dump(X_matrix,open(home_folder+"X_matrix.pkl","wb"))
print("dumping S matrix")
pkl.dump(S_matrix,open(home_folder+"S_matrix.pkl","wb"))