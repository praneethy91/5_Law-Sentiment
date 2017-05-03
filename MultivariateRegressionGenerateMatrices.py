import os
import pickle as pkl
import numpy as np
import pandas as pd

home_folder="/home/bsg348/"
bio_unweighted='bio_unweighted_dict.pkl'
bio_weighted='bio_weighted_dict.pkl'
bio_folder="bioaverage/"
similarity_folder="CircuitYearLevel/"


circuit_year=os.listdir(home_folder+bio_folder)
#this part is hardcoded as we know the data
#and are optimizing time complexity using vectorization
number_of_ckt_years=616
number_of_bio_characteristics=61
number_of_thermometers=40

#creating the input matrices

#Z_matrix represents weighted average biocharacteristic
Z_matrix=np.zeros((number_of_ckt_years*number_of_thermometers,number_of_bio_characteristics))
#X_matrix represents unweighted average biocharacteristic
X_matrix=np.zeros((number_of_ckt_years*number_of_thermometers,number_of_bio_characteristics))
#S_matrix represents the similarity
S_matrix=np.zeros((number_of_ckt_years*number_of_thermometers,1))
counter=0


df = pd.DataFrame(columns=('circuit_thermometer','thermometer_year'))

dataframe_index=0
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
    circuit_year=ckt_yr.split("_")
    circuit_number=circuit_year[0]
    year_number=circuit_year[1]
    for bio_char in file_bio_weighted.keys():
        #print(bio_char)
        Z_matrix[counter:counter+number_of_thermometers,incr]=file_bio_weighted[bio_char]
        #print("abc",file_bio_weighted[bio_char])
        #print("pqr",file_bio_unweighted[bio_char])
        X_matrix[counter:counter+number_of_thermometers,incr]=file_bio_unweighted[bio_char]
        incr += 1


    counter+=number_of_thermometers

    for therm in range(number_of_thermometers):
        print("ck",circuit_number +"_"+ str(therm))
        print("kt",str(therm) + "_"+year_number)
        df.loc[dataframe_index] = [circuit_number +"_"+ str(therm), str(therm)  +"_"+year_number]
        dataframe_index += 1

print("dumping Z matrix")
pkl.dump(Z_matrix,open(home_folder+"Z_matrix.pkl","wb"))
print("dumping X matrix")
pkl.dump(X_matrix,open(home_folder+"X_matrix.pkl","wb"))
print("dumping S matrix")
pkl.dump(S_matrix,open(home_folder+"S_matrix.pkl","wb"))
print(df.iloc[100:200])
dummies_ck=pd.get_dummies(df[['circuit_thermometer']])
dummies_kt=pd.get_dummies(df[['thermometer_year']])
print(dummies_ck.shape)
print(Z_matrix.shape)
print(dummies_kt.shape)
#print(dummies_ck.iloc[0])
#print(dummies_kt.iloc[0])
print("dumping gamma_ck")
pkl.dump(dummies_ck,open("gamma_ck","wb"))
print("dumping gamma_kt")
pkl.dump(dummies_ck,open("gamma_kt","wb"))