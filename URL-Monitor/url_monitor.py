#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import requests
import time

#URL String Inludes InfluxDB Database Name
INFLUX_URL_STRING = 'https://hawk-datasource.tothenew.net/write?db=hawkclient1'
INFLUX_USERNAME = ''
INFLUX_PASSWORD = ''

try:
   weblist={'Prod-LB': 'https://google.com',
           'Prod-Portal': 'https://google.com',
           'Prod-Api': 'https://google.com',
           'Prod-SOAP': 'https://google.com',
           'Prod-Admin': 'https://google.com'
           }
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