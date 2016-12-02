import numpy as np
import pandas as pd 
import csv
import os
import time
from sklearn import metrics
from sklearn.externals import joblib

from constant import Constant
from helper import Helper

class EvaluateModel():

    def getPredictions(self):
        start = time.time()

        fileNameTest = os.environ.get( "FILE_NAME_TEST" )
        modelName = os.environ.get( "MODEL_NAME" )
        modelType = os.environ.get( "MODEL_TYPE", "logistic" )

        modelPath = "{}/{}".format( Constant.MODEL_PATH, modelName )
        model = joblib.load(modelPath)

        testDataPath = "{}/{}".format( Constant.TEST_PATH, fileNameTest )

        dfTest = pd.read_csv( testDataPath, sep = "," )
        predictorColumns = Helper().getPredictorCols( dfTest.columns )

        x = dfTest[ predictorColumns ]
        y = dfTest.Survived

        dfTest["predictedClass"] = model.predict(x)
        predicted = dfTest.predictedClass

        if modelType.lower() in Constant.LOGISTIC.lower():
            coefDf = pd.DataFrame(list(zip(x.columns, np.transpose(model.coef_))))
            print ('Model Coefficients are \n', coefDf)

        print metrics.accuracy_score(y, predicted)
        print metrics.classification_report(y, predicted) 
        print metrics.confusion_matrix(y, predicted) 

        self.savePredictions( dfTest, modelType )

        end = time.time()    
        print ('Total time taken for job (sec) = ', end - start)

    def savePredictions(self, df, modelType):
        fileName = Helper().generateFileName( 
            Constant.FILE_PREFIX, 
            name = "predictions_{}".format( modelType ) 
        )

        filePredPath = "{}/{}.csv".format( Constant.PREDICTIONS_PATH, fileName )
        df.to_csv( path_or_buf = filePredPath, sep=',', index = False  )
        print( 'file {} saved to {}'.format( fileName,  Constant.PREDICTIONS_PATH ) )



EvaluateModel().getPredictions()
