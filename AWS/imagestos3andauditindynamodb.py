#!/usr/bin/python

import os
import uuid
import boto3
from datetime import datetime


#baseDirectory Defination 
#Do not add / at last
#It will pick last directory as Camera Name and process the files inside this directory only.
#Here we can put the list of images 
folderList = ["/tmp/cctv-5/abc/front","/tmp/cctv-5/abc/abcd","/tmp/cctv-5/abc/vats","/tmp/cctv-5/abc/prashant"]
folderLength = len(folderList)

#AWS Credentials
AWS_ACCESS_KEY_ID = '#'
AWS_SECRET_ACCESS_KEY = '#'
REGION = 'us-east-1'
#S3 Bucket Name
BUCKET_NAME = 's3-ttn-random'
#DynamoDB Table Name
TABLE_NAME = 'cctv'


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
dynamodb_client = boto3.client(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION
)


#192.168.88.60_01_20180216154748038_TIMING.jpg
#It will tokenize on the basis of _ and pick 14 digit from file and get date and Time
def getDateTime(fileName):
    return fileName.split('_')[2][:14]

#List only  Files from the Directory
def findfiles(baseDirectory):
    try:
        objects = os.listdir(baseDirectory)  # find all objects in a dir
    except Exception, e:
            print(e)
            return (e.message)
    files = []
    for i in objects:  # check if very object in the folder ...
        if os.path.isfile(baseDirectory +"/"+ i):  # ... is a file.
            files.append(i)  # if yes, append it.
    return files

#Rename the Files by a unique name
def uniqueName():
    return str(uuid.uuid4())

#upload to S3 by different name 
def uploadS3(baseDirectory,fileName,fileExt,s3ObjectKey,s3Bucket):
    filePath = baseDirectory +"/"+ fileName
    try:
        s3Tag='contentType='+str(fileExt)
        with open(filePath, 'rb') as data:
            #s3_client.upload_fileobj(data, s3Bucket, s3ObjectKey)
            response=s3_client.put_object(
                Bucket=s3Bucket,
                Body=data,
                Key=s3ObjectKey,
                Tagging=s3Tag
            )
            #Checking if it is uploaded scuccessfully or not
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print "File Uploded Successfully to S3, Uploading to S3 and delete local file"
                #print "Deleting Local File"
                os.remove(filePath)
            else:
                print "Some error in uploading file to S3"
    except Exception, e:
            print(e)
    return s3ObjectKey

#upload to dynamo DB 
def dynamoDB(cameraName,dateObject,objectKey,tableName,s3ObjectKey):
    try:
        response=dynamodb_client.put_item(
        TableName=tableName, 
        Item={
            'cameraName':{'S':cameraName},
            'date':{'S':dateObject.strftime('%Y-%m-%d')},
            'hour':{'S':dateObject.strftime('%H')},
            'min':{'S':dateObject.strftime('%M')},
            'sec':{'S':dateObject.strftime('%S')},
            'objectKey':{'S':objectKey},
            'webUrl':{'S':s3ObjectKey}
            
        }
        )
        return (response['ResponseMetadata']['HTTPStatusCode'])
    except Exception, e:
            print(e)

def eachCamera(baseDirectory):
    print ("List of Files under :"+baseDirectory.split('/')[-1])
    fileList = findfiles(baseDirectory)
    totalLength = str(len(fileList))
    print fileList
    print ("Total No. of Files :"+totalLength)
    #get camera name
    cameraName = baseDirectory.split('/')[-1]
    for file in fileList:
        print("Processing "+str(fileList.index(file)+1)+" Out of "+totalLength)
        print(file)
        uName = uniqueName()
        #Get the Date and Time from File Name
        dateFormat = getDateTime(file)
        dateObject = datetime.strptime(dateFormat,'%Y%m%d%H%M%S')
        #Get the month and year
        file_month = dateObject.strftime('%Y-%m')
        #Get File Extension
        fileExt = file.split('.')[-1]
        #Create S3 object Key 
        s3ObjectKey = cameraName+"/"+file_month+"/"+uName+"."+fileExt
        print "Writting to DynamoDB"
        objectKey = cameraName+"/"+file
        dynamoDB(cameraName,dateObject,objectKey,TABLE_NAME,s3ObjectKey)
        #print "Uploading to S3 and delete local file"
        uploadS3(baseDirectory,file,fileExt,s3ObjectKey,BUCKET_NAME)

for folder in folderList:
    print("Processing Directory "+str(folder)+" with sequence no." +str(folderList.index(folder)+1)+" Out of "+str(folderLength))
    eachCamera(folder)



    
