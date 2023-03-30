# import numpy as np
# import pickle
# import pandas as pd

# p = np.array([[0,67,145,84,116,128,98,97.8]])
# pickled_model = pickle.load(open('hhcs_rfc.sav', 'rb'))
# print(pickled_model.predict(p))

# fah = 104
# cel = (fah-32)/1.8

# print(cel)

# f=96
# temp = f*9/5+32
# print(temp)


import json
with open('hdata.json') as user_file:
  hdata_c = user_file.read()
parsed = json.loads(hdata_c)
# print(parsed['th'])

with open('physical.json') as user_file:
  physical_c = user_file.read()
physical = json.loads(physical_c)

with open('meditation.json') as user_file:
  meditation_c = user_file.read()
meditation = json.loads(meditation_c)

with open('nutris.json') as user_file:
  nutris_c = user_file.read()
nutris = json.loads(nutris_c)

with open('meds.json') as user_file:
  meds_c = user_file.read()
meds = json.loads(meds_c)


# this changed
with open('syms.json') as user_file:
  syms_c = user_file.read()
syms = json.loads(syms_c)

