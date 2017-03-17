import pandas as pd
import csv
# for displaying all the content on console
pd.options.display.max_rows = 999
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 1000)

itr = pd.read_stata('ANES_raw2008-1948.dta', chunksize=10)

#f = open('ANES_raw2008-1948.dta', 'r')
flag = 1;
for line in itr:
    #print(repr(line))
    with open('ANES_raw2008-1948.csv', 'a') as f:
        if(flag == 1):
            line.to_csv(f)
            flag = 0;
        else:
            line.to_csv(f, header=False)
    #line.to_csv('my_stata_file.csv')
#f.close()
'''
writer = csv.writer(open("test1.csv", "wb"),delimiter = ' ')
for chunk in itr:
    print(chunk);
    writer.writerows(chunk);
'''
'''
import pandas as pd
#data = pd.io.stata.read_stata('ANES_raw2008-1948.dta')
data = pd.read_stata('ANES_raw2008-1948.dta', chunksize=100,convert_categoricals=False, convert_missing=True)
data.to_stata('my_data_out.csv')
#data.to_csv('my_stata_file.csv')
'''
'''
import scikits.statsmodels.api as sm
arr = sm.iolib.genfromdta('/ANES_raw2008-1948.dta')
type(arr)
sm.iolib.savetxt('auto.txt', arr, fmt='%2s', delimiter=",")
'''
