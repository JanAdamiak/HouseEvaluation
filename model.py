import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
import pickle


df = pd.read_csv("C:\\Users\\Jan\\Desktop\\Projects\\Regression_Appartment_model\\Zoopla_data.csv")
df["total_rooms"] = df["bedrooms"] + df["toilets"] + df["other_rooms"]
df = df.dropna()
df = df[df["bedrooms"] > 0]

model = smf.ols("price ~ bedrooms + toilets + other_rooms + C(postcode)", data=df).fit()

pickle.dump(model, open("regression_model.sav", "wb"))
