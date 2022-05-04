import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import clear_output

#Load dataset
df_true = pd.read_csv('C:\\Users\\Ben\\Desktop\\True.csv', nrows=555)
df_false = pd.read_csv('C:\\Users\\Ben\\Desktop\\Fake.csv', nrows=555)
df_false.drop(df_false.iloc[:,5:173],1,inplace=True)#Correction de la dataset false

df_train = pd.concat([df_true, df_false], axis=0)#Dataset train

df_true_e = pd.read_csv('C:\\Users\\Ben\\Desktop\\True.csv', nrows=50)
df_false_e = pd.read_csv('C:\\Users\\Ben\\Desktop\\Fake.csv', nrows=50)
df_false_e.drop(df_false_e.iloc[:,5:173],1,inplace=True)#Correction de la dataset false_e

df_eval = pd.concat([df_true_e, df_false_e], axis=0)#Dataset eval

df_true_p = pd.read_csv('C:\\Users\\Ben\\Desktop\\True.csv',skiprows=550, nrows=5)
df_false_p = pd.read_csv('C:\\Users\\Ben\\Desktop\\Fake.csv',skiprows=550, nrows=5)
df_false_p.drop(df_false_p.iloc[:,5:173],1,inplace=True)#Correction de la dataset false_p

df_pred = pd.concat([df_true_p, df_false_p], axis=0)#Dataset predict
#df_res = df_pred.pop('State')
print(df_eval.head())