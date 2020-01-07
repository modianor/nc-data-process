# *_*coding:utf-8 *_*

import numpy as np
from netCDF4 import Dataset, OrderedDict

dataset:Dataset = Dataset(filename='nc_data/NC_H08_20160701_0530_L2CLPbet_FLDK.02401_02401.nc', mode='r')

variables:OrderedDict = dataset.variables

keys = variables.keys()

print(keys)

latitude = np.array(variables['latitude'])
longitude = np.array(variables['longitude'])

print(latitude.tolist())
print(longitude.tolist())




