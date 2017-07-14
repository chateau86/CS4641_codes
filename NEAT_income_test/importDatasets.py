import pandas as pd

def iD(filename):
    if filename == "preprocessed_ID.csv":
        data = pd.read_csv("preprocessed_ID.csv", header=0)
        data.drop("Unnamed: 0", axis=1, inplace=True)
        Y = data.Prediction.values
        data.drop("Prediction", axis=1, inplace=True)
        X = data.values
    elif filename == "scaled_voice.csv":
        data = pd.read_csv("scaled_voice.csv", header=0)
        data.drop("Unnamed: 0", axis=1, inplace=True)
        Y = data.label.values
        data.drop('label', axis=1, inplace=True)
        X = data.values
    return (X,Y)
