import numpy as np
import pandas as pd 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import csv
import os
import time

from constant import Constant
from helper import Helper

import pickle
from sklearn.externals import joblib

class BuildModel():

    def saveModel(self):
        start = time.time()

        fileNameTrain = os.environ.get( "FILE_NAME_TRAIN" )
        modelType = os.environ.get( "MODEL_TYPE", "logistic" )

        trainDataPath = "{}/{}".format( Constant.TRAIN_PATH, fileNameTrain )

        dfTrain = pd.read_csv( trainDataPath, sep = "," )
        predictorColumns = Helper().getPredictorCols( dfTrain.columns )

        x = dfTrain[ predictorColumns ]
        y = dfTrain.Survived

        if modelType.lower() in Constant.LOGISTIC.lower():
            model = LogisticRegression()
            model.fit(  x,  y  )
        else:
            random_state = np.random.RandomState(0)
            model = RandomForestClassifier(
                         n_estimators=30, 
                         max_depth=None, 
                         warm_start=False,                                
                         criterion='gini', 
                         max_features='auto', 
                         max_leaf_nodes=None, 
                         min_samples_leaf=1, 
                         min_samples_split=2, 
                         min_weight_fraction_leaf=0.0, 
                         oob_score=True, 
                         random_state=random_state
                        )
            model.fit( x, y )

        modelName = Helper().generateFileName( Constant.FILE_PREFIX, name = "model_{}".format(modelType) )

        path = "{}/{}.pkl".format( Constant.MODEL_PATH, modelName )
        joblib.dump( model, path ) 

        print( 'file {} saved to {}'.format( modelName,  Constant.MODEL_PATH ) )

        end = time.time()    
        print ( 'Total time taken for job (sec) = ', end - start )


BuildModel().saveModel()
