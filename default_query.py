import datetime

# # query for debugging, returns relatively quickly
# query = '_sourcecategory="prod/activity/application/cas" !"net.unicon" !"150.108*" !"83.216.90.28" !"193.61.71.138" !"108.179.53.194" |timeslice 1h | lookup latitude, longitude, country_name,city from geo://location on ip = src_ip | where [subquery: _sourcecategory="prod/activity/application/cas" !"net.unicon" !"150.108*" !"83.216.90.28" !"193.61.71.138" !"108.179.53.194" | timeslice 1h | where !(username matches "*ttest*" OR username matches "*.*" OR username matches "FITADMINQUERY") | where !compareCIDRPrefix("150.108.0.0", src_ip, toInt(16)) | where action="Authentication Success" or action="Authentication Failure" | lookup latitude, longitude, country_name,city from geo://location on ip = src_ip | count_distinct (username) group by _timeslice,src_ip,country_name | where _count_distinct > 4 |compose src_ip,_timeslice,country_name] | where action="Authentication Success" |concat("https://www.abuseipdb.com/check/",src_ip) as abuse_lookup | concat ("https://mxtoolbox.com/SuperTool.aspx?action=arin%3a",src_ip,"&run=toolpage") as owner_lookup | count by _timeslice,username,action,src_ip,country_name,abuse_lookup,owner_lookup'
# fromTime = "2019-01-15T00:00:00"
# toTime = "2019-01-15T02:00:00"
# timeZone = "EST"

#default query if not retrieving query_results from sys parameter
query = '' #SumoLogic query with src_ip field
d = datetime.datetime.now()
s = d.strptime(d.strftime("%Y:%m:%d"),"%Y:%m:%d") + datetime.timedelta(days=-1) #fromTime cannot be larger than toTime
t = str(s.strftime("%H:%M:%S"))
fromTime = str(d.strftime("%Y-%m-%dT")) + t               #negative days before current time
toTime = d.strftime("%Y-%m-%dT") + d.strftime("%H:%M:%S") #current time
timeZone = "EST"
