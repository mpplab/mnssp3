import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import Sequential 
from keras import layers 
from keras import regularizers
from sklearn.model_selection import train_test_split 
from sklearn.metrics import roc_curve, auc
from keras.models import load_model


def main(data_path, model_path):
    df = pd.read_csv(data_path, header=0, index_col=0)
    if 'y' in df.columns.values:
        df1 = df.drop("y", axis=1)
    else:
        df1 = df
    wave = np.zeros((len(df1), 178))

    z=0
    for index, row in df1.iterrows():
        wave[z,:] = row
        z += 1

    # model = load_model('model_save/epilepsy_detection_model_x.h5')
    model = load_model(model_path)

    res = model.predict(wave).ravel()
    res_ctrl = []
    for i in res:
        if i > 0.5:
            res_ctrl.append(1)
        else:
            res_ctrl.append(0)

    return res_ctrl
	# return res


if __name__ == "__main__":
    data_path = sys.argv[1]
    try:
        model_path = sys.argv[2]
    except IndexError:
        model_path = 'C:/wamp64/www/EEG/model_save/epilepsy_detection_model_x.h5'
    res = main(data_path, model_path)
    print(res)

