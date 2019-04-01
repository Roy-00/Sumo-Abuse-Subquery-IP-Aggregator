import sys
import json
import os
from api_keys import *
from default_query import *
from sumologic import *
from abuseipdb import AbuseIPDB

def results(query_results,joined_results,autoQuery,console_show_join=False):
    directory = "./logs"
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
    if console_show_join == True:
        print("Joined Results: " + '\n' + json.dumps(joined_results))
    file = open(directory + "/output_" + d.strftime("D%Y-%m-%d_") + d.strftime("T%H-%M-%S") + "_.txt", "w")
    file.write("autoQuery = " + str(autoQuery) + '\n\n')
    if autoQuery == True:
        file.write("Query:\n" + query + '\n\n')
        file.write("From " + fromTime + " to " + toTime + '\n\n')
    file.write("Query Results:\n")
    file.write(json.dumps(query_results) + '\n\n')
    file.write("Joined Results:\n")
    file.write(json.dumps(joined_results))
    file.close()

def fail_search(exception):
    directory = "./logs"
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
    file = open(directory + "/output_" + d.strftime("D%Y-%m-%d_") + d.strftime("T%H-%M-%S") + "_.txt", "w")
    file.write("autoQuery = " + str(autoQuery) + '\n\n')
    file.write("FAILED SEARCH" + '\n\n')
    file.write("EXCEPTION:\n" + str(exception) + '\n\n')
    if autoQuery == True:
        file.write("Query:\n" + query + '\n\n')
        file.write("From " + fromTime + " to " + toTime + '\n\n')
    file.close()

def get_ip_list(query_results):
    ip_list = []
    for dictionary in query_results:
        for key, value in dictionary.items():
            if key == 'src_ip':
                ip_list.append(value)
    return ip_list

def join(ip_records, query_results):
    joined_results = []
    for record, dictionary in zip(ip_records, query_results):
        record = record.getAttributes(includeIP=False)
        temp = {}
        for key, value in record.items():
            temp[key + " (abuseIPDB)"] = value
        join = {**dictionary, **temp}
        joined_results.append(join)
    return joined_results

def get_query_results(sumo_api,query,fromTime,toTime,timeZone,autoQuery,showQuery=True):
    if autoQuery == False:
        if sys.argv[0] != "main.py":
            query_results_path = sys.argv[0]
        else:
            query_results_path = sys.argv[1]
        print("Accessing Sumo Search Results in: " + str(query_results_path) + '\n')
        with open(str(query_results_path)) as file:
            query_results = json.load(file)
    else:
        print("Query: " + query + '\n')
        print("From " + fromTime + " to " + toTime + '\n')
        try:
            query_results = sumo_api.search(query,fromTime=fromTime,toTime=toTime,timeZone=timeZone)
        except Exception as e:
            fail_search(e)
    print("Query Results: \n" + str(query_results) + '\n')
    return query_results

def main():
    sumo_api = SumoLogic(sumo_access_id, sumo_access_key)

    if sys.argv[0] == "main.py":
        try:
            sys.argv[1]
        except:
            autoQuery = True
        else:
            autoQuery = False
    if sys.argv[0] != "main.py":
        autoQuery = False

    query_results = get_query_results(sumo_api,query,fromTime,toTime,timeZone,autoQuery,showQuery=True)

    ipAddresses = get_ip_list(query_results)

    abuseipdb_api = AbuseIPDB()
    days = '1'
    ip_records = []

    for ip in ipAddresses:
        json_load = abuseipdb_api.check_ip(ip, days, abuse_apiV2_key)
        ip_records.append(abuseipdb_api.record_ip_data(json_load))

    joined_results = join(ip_records, query_results)

    results(query_results,joined_results,autoQuery,console_show_join=True)

if __name__ == '__main__':
    main()
