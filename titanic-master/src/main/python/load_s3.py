import os
import time

import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

import shutil

class LoadS3():

    def __init__(self):

        self.awsBucket = os.environ.get( "AWS_BUCKET" )
        self.filePath = os.environ.get( "FILE_PATH" )

        print( "your file path is {}".format(self.filePath)  )

        if self.awsBucket == None:
            raise Exception("Missing one or more parameters, please reenter")
		
    def toS3(self):
		
        fileNames = os.listdir(self.filePath) # returns list of paths (list of strings)
         
        conn = S3Connection()
        bucket = conn.lookup(self.awsBucket)

        for fileName in fileNames:
            k = Key(bucket)
            k.key = fileName
            filePath = "{}/{}".format(self.filePath,fileName)
            k.set_contents_from_filename(filePath, encrypt_key = True)


LoadS3().toS3()

