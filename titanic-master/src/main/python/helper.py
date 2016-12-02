import time
from constant import Constant

class Helper:
	def generateFileName(self, prefix, name): 
		timestamp = time.strftime("%m:%d:%y:%H:%M:%S")
		fileName = "{}_{}_{}".format( prefix, name, timestamp )
                return fileName

        def getPredictorCols(self,dfColumns): 
        	predictorColumns = filter( self.checkForLabelCol, dfColumns.tolist() )
       	        return predictorColumns

        def checkForLabelCol(self,column):
    	        return column.lower() not in Constant.LABEL_COL.lower() 

