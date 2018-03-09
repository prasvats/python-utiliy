#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import requests
import time

#URL String Inludes InfluxDB Database Name
INFLUX_URL_STRING = 'https://influx.verecloud.com/write?db=test'
INFLUX_USERNAME = 'influx'
INFLUX_PASSWORD = 'inmemory'

try:
   weblist={'Prod-LB': 'https://bluesky.westconcomstor.com/resources/build_artifact.json',
           'Prod-Portal': 'http://wc-proxy-prod/resources/build_artifact.json',
           'Prod-Api': 'http://wcprod-bluesky:8080/nimbus4-api/build_artifact.json',
           'Prod-SOAP': 'http://wcprod-bluesky-soap:8080/nimbus4-soap/build_artifact.json',
           'Prod-Admin': 'http://wcprod-bluesky-B:8080/nimbus4-admin/build_artifact.json',
           'Prod-Backend': 'http://wcprod-bluesky-apps:8080/nimbus4-backend/build_artifact.json',
           'Prod-Backend-2': 'http://wcprod-bluesky-apps-B:8080/nimbus4-backend/build_artifact.json',
           'Prod-OAuth': 'http://wcprod-bluesky:3000/oauth20/applications'}
   data =[]

   def getEpochTime():
        #Make it 19 Digit Epoch Time   
        timeObject = int(time.time())
        objectLength = len(str(timeObject))
        return timeObject*10**(19-objectLength)


   print "---------START-----------"
   for row in weblist.keys():
       print "<!----Data---!>"
       statusCode=elapsedTime="NULL"
       try:
               r = requests.get(weblist[row],timeout=40)
               statusCode=r.status_code
               elapsedTime=r.elapsed.total_seconds()
               #print statusCode, elapsedTime
              
       except requests.exceptions.RequestException as e:  # This is the correct syntax
               statusCode="500"
               elapsedTime="40.1"
               #print statusCode, elapsedTime

       url_string = INFLUX_URL_STRING
       data_string = 'Status,App='+str(row)+' StatusCode='+str(statusCode)+',TimeElapsed='+str(elapsedTime)+' '+str(getEpochTime())
       print data_string
       post = requests.post(url_string, data=data_string, auth=(INFLUX_USERNAME, INFLUX_PASSWORD))
       print "InfluxDB Post Status Code:"+str(post.status_code)
   print "-----------END------------"
except (RuntimeError, TypeError, NameError) as e:
   print e
