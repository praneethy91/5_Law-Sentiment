import os
import pickle as pkl
import numpy as np
import pandas as pd
import functools

home_folder="data/"
bio_unweighted='bio_unweighted_dict.pkl'
bio_weighted='bio_weighted_dict.pkl'
bio_folder="bioaverage/"
similarity_folder="CircuitYearLevel/"
anes_folder = "outcome_var/"

def cmp_items(a, b):
    m = a.split("_")
    circuit_a = int(m[0])
    year_a = int(m[1])

    s = b.split("_")
    circuit_b = int(s[0])
    year_b = int(s[1])

    if circuit_a > circuit_b:
        return 1
    elif circuit_a == circuit_b:
        if year_a > year_b:
            return 1
        else:
            return -1
    else:
        return -1

circuit_year = os.listdir(home_folder+anes_folder)
circuit_year = sorted(circuit_year, key=functools.cmp_to_key(cmp_items))

#this part is hardcoded as we know the data
#and are optimizing time complexity using vectorization
number_of_ckt_years=248 # got from ANES data
number_of_bio_characteristics=61
number_of_thermometers=40

#creating the input matrices

# Z_matrix represents weighted average biocharacteristic
Z_matrix=np.zeros((number_of_ckt_years*number_of_thermometers,number_of_bio_characteristics))

# Y_matrix is the outcome variable
Y_matrix = np.zeros((number_of_ckt_years*number_of_thermometers,1))

# S_matrix represents the similarity
S_matrix=np.zeros((number_of_ckt_years*number_of_thermometers,1))
counter=0

<<<<<<< HEAD

df = pd.DataFrame(columns=('circuit_thermometer','thermometer_year','circuit_year'))
=======
df = pd.DataFrame(columns=('circuit_thermometer','thermometer_year', 'circuit_year'))
>>>>>>> d39d2bea1b4fd7f99da463499ee59d86e53884ae

dataframe_index=0
for ckt_yr in circuit_year:
    # generate the outcome variable vector

    name_file_similarity=home_folder+similarity_folder+ckt_yr+".0.p"
    name_file_bio_weighted=home_folder+bio_folder+ckt_yr+"/"+bio_weighted
    name_output_scores = home_folder+anes_folder+ckt_yr+"/outcome_score"
    file_similarity = pkl.load(open(name_file_similarity,'rb'))
    outcome_scores = pkl.load(open(name_output_scores,'rb'))

    file_bio_weighted=pkl.load(open(name_file_bio_weighted,'rb'))
    #print("abc",file_bio_weighted['x_phouse'])
    S_matrix[counter:counter+number_of_thermometers]=file_similarity.reshape((number_of_thermometers,1))

    outcome_scores_reshape = outcome_scores.reshape((number_of_thermometers, 1))
    Y_matrix[counter:counter + number_of_thermometers] = outcome_scores_reshape

    incr=0
    circuit_year=ckt_yr.split("_")
    circuit_number=circuit_year[0]
    year_number=circuit_year[1]
    for bio_char in sorted(file_bio_weighted.keys()):
        #print(bio_char)
        Z_matrix[counter:counter+number_of_thermometers,incr]=file_bio_weighted[bio_char]
        incr += 1

    counter+=number_of_thermometers

    for therm in range(number_of_thermometers):
<<<<<<< HEAD
        print("ck",circuit_number +"_"+ str(therm))
        print("kt",str(therm) + "_"+year_number)
        df.loc[dataframe_index] = [circuit_number +"_"+ str(therm), str(therm)  +"_"+year_number,circuit_number+"_"+year_number]
=======
        # print("ck",circuit_number +"_"+ str(therm))
        # print("kt",str(therm) + "_"+year_number)
        df.loc[dataframe_index] = [circuit_number +"_"+ str(therm), str(therm)  +"_"+year_number, circuit_number +"_"+ year_number]
>>>>>>> d39d2bea1b4fd7f99da463499ee59d86e53884ae
        dataframe_index += 1

stacked_matrix = np.column_stack((Z_matrix, S_matrix, Y_matrix))
rows_notnan = np.where(np.all(~np.isnan(stacked_matrix), axis=1))[0]
stacked_matrix = stacked_matrix[~np.isnan(stacked_matrix).any(axis=1)]
print(stacked_matrix[:, -1][0:200])

Z_matrix = stacked_matrix[:, 0:number_of_bio_characteristics]
S_matrix = stacked_matrix[:, -2]
Y_matrix = stacked_matrix[:, -1]

print("dumping Z matrix")
pkl.dump(Z_matrix,open(home_folder+"Z_matrix.pkl","wb"))
print("dumping S matrix")
pkl.dump(S_matrix,open(home_folder+"S_matrix.pkl","wb"))
print("dumping Y matrix")
pkl.dump(Y_matrix,open(home_folder+"Y_matrix.pkl","wb"))

dummies_ck=pd.get_dummies(df[['circuit_thermometer']])
dummies_ck = dummies_ck.ix[rows_notnan]
dummies_kt=pd.get_dummies(df[['thermometer_year']])
<<<<<<< HEAD
dummies_ct=pd.get_dummies(df[['circuit_year']])
print(dummies_ck.shape)
=======
dummies_kt = dummies_kt.ix[rows_notnan]
dummies_ct=pd.get_dummies(df[['circuit_year']])
dummies_ct = dummies_ct.ix[rows_notnan]

>>>>>>> d39d2bea1b4fd7f99da463499ee59d86e53884ae
print(Z_matrix.shape)
print(S_matrix.shape)
print(Y_matrix.shape)
print("-----------------------")
print(dummies_ck.shape)
print(dummies_kt.shape)
print(dummies_ct.shape)

#print(dummies_ck.iloc[0])
#print(dummies_kt.iloc[0])

print("dumping gamma_ck")
pkl.dump(dummies_ck,open(home_folder+"gamma_ck","wb"))
print("dumping gamma_kt")
<<<<<<< HEAD
pkl.dump(dummies_kt,open(home_folder+"gamma_kt","wb"))
print("dumping gamma_ct")
pkl.dump(dummies_ct,open(home_folder+"gamma_ct","wb"))
=======
pkl.dump(dummies_ck,open(home_folder+"gamma_kt","wb"))
print("dumping gamma_ct")
pkl.dump(dummies_ck,open(home_folder+"gamma_ct","wb"))
>>>>>>> d39d2bea1b4fd7f99da463499ee59d86e53884ae
