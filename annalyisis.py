from os import listdir
from os.path import isfile, join
import numpy as np

mypath = "./SortTest"
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
codes =  []
for a in filenames:
    codes.append(a[:12])
