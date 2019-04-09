import datetime

# # query for debugging, returns relatively quickly
# query = ''
# fromTime = "2019-01-15T00:00:00"
# toTime = "2019-01-15T02:00:00"
# timeZone = "EST"

#default query if not retrieving query_results from sys parameter
query = '' #SumoLogic query with src_ip field
current_date = datetime.datetime.now()
delta = current_date.strptime(current_date.strftime("%Y:%m:%d"),"%Y:%m:%d") + datetime.timedelta(days=-1) #fromTime cannot be larger than toTime
time = str(delta.strftime("%H:%M:%S"))
fromTime = str(current_date.strftime("%Y-%m-%dT")) + time  #negative days before current time
toTime = current_date.strftime("%Y-%m-%dT") + current_date.strftime("%H:%M:%S") #current time
timeZone = "EST"
