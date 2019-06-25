import numpy as np
import  pandas as pd
import  h5py
import re

import pybel
from tfbio.data import Featurizer
import os

import warnings

import matplotlib.pyplot as plt
import seaborn as sns


test_set = pd.read_csv ("./random811/test.csv")
validation_set = pd.read_csv ("./random811/valid.csv")
training_set = pd.read_csv("./random811/train.csv")

print (test_set["pKd/pKi"].isnull().any())

featurizer = Featurizer ()
charge_idx = featurizer.FEATURE_NAMES.index('partialcharge')

ds_path = "./refined-set"
list = os.listdir(ds_path)
for i in range(0,len(list)):
    path = os.path.join(ds_path,list[i])
    if os.path.isdir(path) and re.search("\d\w\d\w",path):
        p_file = os.listdir(path)
        for f in p_file:
            ligand = []
            pocket = []
            if re.match("\d\w\d\w_ligand\.mol2",f):
                print ('%s/%s' % (path, f))
                ligand = next(pybel.readfile('mol2', '%s/%s' % (path, f)))
            if re.match("\d\w\d\w_pocket\.mol2",f):
                print ('%s/%s' % (path, f))
                pocket = next(pybel.readfile('mol2', '%s/%s/' % (path,f)))
            ligand_coords, ligand_features = featurizer.get_features(ligand, molcode=1)
            assert (ligand_features[:, charge_idx] != 0).any()
            pocket_coords, pocket_features = featurizer.get_features(pocket, molcode=-1)
            assert (pocket_features[:, charge_idx] != 0).any()
            centroid = ligand_coords.mean(axis=0)
            ligand_coords -= centroid
            pocket_coords -= centroid
            data = np.concatenate((np.concatenate((ligand_coords, pocket_coords)),
                                   np.concatenate((ligand_features, pocket_features))), axis=1)

