import pandas as pd
import numpy as np
import csv
from types import *
with open('outcome_variables.csv', 'rb') as f:
    reader = csv.reader(f)
    i = 0;
    YCKT = [];
    for row in reader:
        if(i != 0):
            inter = [];
            for j in row:
                if(j != ''):
                    inter.append(float(j));
                else:
                    inter.append(np.nan);
            YCKT.extend(inter);
            #results = map(float, row)
        i = 1;
    print np.shape(YCKT);
