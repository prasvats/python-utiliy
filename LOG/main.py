#!/usr/bin/env python
"""
USAGE:

python main.py 

"""

import sys
import re
import datetime
import time
#import redis
start_time = time.time()

REDIS_HOST="10.1.52.67"
REDIS_KEY="test-log-sel"
dateFormat = '%Y-%m-%d %H:%M:%S:%f'
sleep = 300
currentTime=datetime.datetime.now()
checkpointTime=datetime.datetime.now() - datetime.timedelta(seconds=sleep)

fname ="/var/log/abc.log"

def modifytimestamp(timestamp):
    year = str(datetime.date.today().year)
    s = year+" "+str(timestamp) 
    e= '%Y %d %b %H:%M:%S'
    return datetime.datetime.strptime(s, e)
    #return datetime.datetime.strftime(d, dateFormat)


def getTimeViaRegex(line):
    myregex=r'[0-9]{2} [A-Za-z]{3} [0-9]{2}:[0-9]{2}:[0-9]{2}'
    if re.search(myregex, line):
        #print 'found a match!'
        originalTimestamp=re.search(myregex,line).group(0)
        modifiedTimeStamp=modifytimestamp(originalTimestamp)
        #print modifiedTimeStamp
        return modifiedTimeStamp
    else:
        #print 'no match'
        #print line
        return None
    

def getfromfile(fname,CHUNK=1024*1024):
    with open(fname, "r") as f:
        f.seek (0, 2)      
        fsize = f.tell()       
        f.seek (max (fsize-CHUNK, 0), 0)
        lines = f.readlines()
    return lines  


def analyze_log(lines):
    final_log=[]
    for line in lines:
        #print line
        timestamp=getTimeViaRegex(line)
        if (timestamp!=None and (timestamp >= checkpointTime)):
            timestamp=timestamp+datetime.timedelta(milliseconds=datetime.datetime.now().microsecond)
            final_log.append({'@timestamp':timestamp.strftime(dateFormat),'message':line})
    return final_log


def dumpToRdis(data):
    conn = redis.Redis(REDIS_HOST)
    conn.hmset(REDIS_KEY, data)

if __name__ == "__main__":
    #analyze_log(getfromfile(fname))
    data=analyze_log(getfromfile(fname))
    print data
    #dumpToRdis(data)
    print("--- %s Total Execution Time seconds ---" % (time.time() - start_time))

    