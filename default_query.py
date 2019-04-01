import datetime

#default query if not retrieving query_results from sys parameter
query = '' #SumoLogic query with src_ip field
d = datetime.datetime.now()
s = d.strptime(d.strftime("%Y:%m:%d"),"%Y:%m:%d") + datetime.timedelta(days=-1) #fromTime cannot be larger than toTime
t = str(s.strftime("%H:%M:%S"))
fromTime = str(d.strftime("%Y-%m-%dT")) + t               #negative days before current time
toTime = d.strftime("%Y-%m-%dT") + d.strftime("%H:%M:%S") #current time
timeZone = "EST"
