import sys
import json
import os
from abuseipdb import AbuseIPDB
from sumologic import SumoLogic

class SumoLogic_AbuseIPDB_Aggregator():
    def __init__(self):
        """
        Checks for command line arguements
        Input (None):
            sys.argv[]                       : System command line arguemnts
        Return (None):
            query (String)                   : The SumoLogic query
            defaultQuery (Bool)              : Indicates if default query was executed
            fromTime (String)                : Date for query to start search
            toTime (String)                  : Date for query to end search
            timeZone (String)                : Timezone so query knows what timezone to align its search times to
            current_date (String)            : Today's date
            uniqueHTTPCollectorCode (String) : The code for the collector to post to
            sumo_access_id (String)          : Needed to access SumoLogic through Sumo Logic Python SDK
            sumo_access_key (String)         : Needed to access SumoLogic through Sumo Logic Python SDK
            abuse_apiV2_key (String)         : Needed to access AbuseIPDB api
            abuseIPDB_days (String)          : Number of days AbuseIPDB api will use when looking up ip
        """
        try:
            sys.argv[1] #query assignment
        except:
            sys.exit("Status Code 1\n1 parameters is missing (query).")
        else:
            if sys.argv[1] == "default-all":
                self.defaultQuery = True
                from default_query import query
                if not query:
                    sys.exit("Status Code 1\n1 parameters is missing in defaults (query).")
                self.query = query
                from default_query import current_date,fromTime,toTime,timeZone
                if not fromTime or not toTime or not timeZone or not current_date:
                    sys.exit("Status Code 1\nAt least 1 time parameters is missing in defaults (fromTime, toTime, timeZone, or current_date).")
                self.fromTime = fromTime
                self.toTime = toTime
                self.timeZone = timeZone
                self.current_date = current_date
                from sumo_collector_code import uniqueHTTPCollectorCode
                if not uniqueHTTPCollectorCode:
                    sys.exit("Status Code 1\nAt least 1 parameters is missing in defaults (uniqueHTTPCollectorCode).")
                self.uniqueHTTPCollectorCode = uniqueHTTPCollectorCode
                self.postAuthorization = True
                from api_keys import sumo_access_id,sumo_access_key
                if not sumo_access_id or not sumo_access_key:
                    sys.exit("Status Code 1\nAt least 1 sumo access parameters is missing  in defaults (sumo_access_id or sumo_access_key).")
                self.sumo_access_id = sumo_access_id
                self.sumo_access_key = sumo_access_key
                self.sumo_api = SumoLogic(sumo_access_id,sumo_access_key)
                from api_keys import abuse_apiV2_key
                if not abuse_apiV2_key:
                    sys.exit("Status Code 1\nAt least 1 parameters is missing in defaults (abuse_apiV2_key).")
                self.abuse_apiV2_key = abuse_apiV2_key
                from abuseipdb_parameters import abuseIPDB_days
                if not abuseIPDB_days:
                    sys.exit("Status Code 1\nAt least 1 parameters is missing in defaults (abuseIPDB_days).")
                self.abuseIPDB_days = abuseIPDB_days
                self.log_directory = "./logs"
                return
            elif sys.argv[1] == "default":
                self.defaultQuery = True
                from default_query import query
                if not query:
                    sys.exit("Status Code 1\n1 parameters is missing in defaults (query).")
                self.query = query
            else:
                self.defaultQuery = False
                with open(str(sys.argv[1])) as file:
                    self.query = str(file.read())

        try:
            sys.argv[2] #fromTime assignment
            sys.argv[3] #toTime assignment
            sys.argv[4] #timeZone assignment
        except:
            sys.exit("Status Code 1\nAt least 1 time parameters is missing (fromTime, toTime, or timeZone).")
        else:
            if sys.argv[2] == sys.argv[3] == sys.argv[4] == "default":
                from default_query import current_date,fromTime,toTime,timeZone
                if not fromTime or not toTime or not timeZone or not current_date:
                    sys.exit("Status Code 1\nAt least 1 time parameters is missing in defaults (fromTime, toTime, timeZone, or current_date).")
                self.fromTime = fromTime
                self.toTime = toTime
                self.timeZone = timeZone
                self.current_date = current_date
            elif sys.argv[2] or sys.argv[3] or sys.argv[4] != "default" and sys.argv[2] or sys.argv[3] or sys.argv[4] == "default":
                sys.exit("Status Code 1\nAll parameters must be default or inputted (fromTime, toTime, or timeZone).")
            else:
                from default_query import current_date
                if not current_date:
                    sys.exit("Status Code 1\nAt least 1 time parameters is missing in defaults (current_date).")
                self.fromTime = sys.argv[2]
                self.toTime = sys.argv[3]
                self.timeZone = sys.argv[4]
                self.current_date = current_date

        try:
            sys.argv[5] #uniqueHTTPCollectorCode assignment
        except:
            sys.exit("Status Code 1\nAt least 1 parameters is missing (uniqueHTTPCollectorCode).")
        else:
            if sys.argv[5] == "default":
                from sumo_collector_code import uniqueHTTPCollectorCode
                if not uniqueHTTPCollectorCode:
                    sys.exit("Status Code 1\nAt least 1 parameters is missing in defaults (uniqueHTTPCollectorCode).")
                self.uniqueHTTPCollectorCode = uniqueHTTPCollectorCode
                self.postAuthorization = True
            elif sys.argv[5] == "False":
                self.uniqueHTTPCollectorCode = ""
                self.postAuthorization = False
            else:
                self.uniqueHTTPCollectorCode = sys.argv[5]
                self.postAuthorization = True

        try:
            sys.argv[6] #sumo_access_id assignment
            sys.argv[7] #sumo_access_key assignment
        except:
            sys.exit("Status Code 1\nAt least 1 sumo access parameters is missing (sumo_access_id or sumo_access_key).")
        else:
            if sys.argv[6] == sys.argv[7] == "default":
                from api_keys import sumo_access_id,sumo_access_key
                if not sumo_access_id or not sumo_access_key:
                    sys.exit("Status Code 1\nAt least 1 sumo access parameters is missing  in defaults (sumo_access_id or sumo_access_key).")
                self.sumo_access_id = sumo_access_id
                self.sumo_access_key = sumo_access_key
                self.sumo_api = SumoLogic(sumo_access_id,sumo_access_key)
            elif sys.argv[6] == "default" and sys.argv[7] != "default" or sys.argv[6] != "default" and sys.argv[7] == "default":
                sys.exit("Status Code 1\nBoth parameters must be default or inputted (sumo_access_id or sumo_access_key).")
            else:
                self.sumo_access_id = sys.argv[6]
                self.sumo_access_key = sys.argv[7]
                self.sumo_api = SumoLogic(self.sumo_access_id,self.sumo_access_key)

        try:
            sys.argv[8] #abuse_apiV2_key assignment
        except:
            sys.exit("Status Code 1\nAt least 1 parameters is missing (abuse_apiV2_key).")
        else:
            if sys.argv[8] == "default":
                from api_keys import abuse_apiV2_key
                if not abuse_apiV2_key:
                    sys.exit("Status Code 1\nAt least 1 parameters is missing in defaults (abuse_apiV2_key).")
                self.abuse_apiV2_key = abuse_apiV2_key
            else:
                self.abuse_apiV2_key = sys.argv[8]

        try:
            sys.argv[9] #abuseIPDB_days assignment
        except:
            sys.exit("Status Code 1\nAt least 1 parameters is missing (abuseIPDB_days).")
        else:
            if sys.argv[9] == "default":
                from abuseipdb_parameters import abuseIPDB_days
                if not abuseIPDB_days:
                    sys.exit("Status Code 1\nAt least 1 parameters is missing in defaults (abuseIPDB_days).")
                self.abuseIPDB_days = abuseIPDB_days
            else:
                self.abuseIPDB_days = sys.argv[9]

        try:
            sys.argv[10] #log_directory assignment
        except:
            sys.exit("Status Code 1\nAt least 1 parameters is missing (log_directory).")
        else:
            if sys.argv[10] == "default":
                self.log_directory = "./logs"
            else:
                self.log_directory = sys.argv[10]

    def abuseIPDB_lookup(self,ipAddresses):
        abuseipdb_api = AbuseIPDB()
        ip_records = []

        for ip in ipAddresses:
            json_load = abuseipdb_api.check_ip(ip, self.abuseIPDB_days, self.abuse_apiV2_key)
            ip_records.append(abuseipdb_api.record_ip_data(json_load))

        return ip_records

    def record_search(self,query_results,joined_results,console_show_join=False,return_fileName=False):
        """
        Populates file with log info and the parameters passed in
        Input:
            query_results (List)     : List of dictionaries containing the results of the SumoLogic query
            joined_results (List)    : query_results with abuseIPDB results joined into each dictionary
            console_show_join (Bool) : Indicates whether joined_results will be printed in console
            return_fileName (Bool)   : Indicates whether file name of log is returned
        Return:
            file_name (String)       : The file name of the log that was just recorded
        """
        try:
            if not os.path.exists(self.log_directory):
                os.makedirs(self.log_directory)
        except OSError:
            print ('Error: Creating directory. ' +  self.log_directory)

        file_name = self.log_directory + "/output_" + self.current_date.strftime("D%Y-%m-%d_") + self.current_date.strftime("T%H-%M-%S") + "_.txt"

        if console_show_join is True:
            print("Joined Results: " + '\n' + json.dumps(joined_results))

        file = open(file_name, "w")
        file.write("defaultQuery = " + str(self.defaultQuery) + '\n\n')

        if self.defaultQuery is False:
            file.write("Accessing Sumo Search Query in: " + str(sys.argv[1]) + '\n\n')
        else:
            file.write("Accessing Sumo Search Query in: default_query.py" + '\n\n')

        file.write("Query:\n" + self.query + '\n\n')
        file.write("From " + self.fromTime + " To " + self.toTime + '\n\n')
        file.write("Query Results:\n")
        file.write(json.dumps(query_results) + '\n\n')
        file.write("Joined Results:\n")
        file.write(json.dumps(joined_results))
        file.close()

        if return_fileName is True:
            return file_name

    def failed_search(self,exception,query_results,console_show_join=False):
        """
        Populates file with log info and the parameters passed in upon failed search and kills execution
        Input:
            exception (String)       : The Exception raised
            console_show_join (Bool) : Indicates whether joined_results will be printed in console
        Return (None):
            Kills execution after logging to file
        """
        try:
            if not os.path.exists(self.log_directory):
                os.makedirs(self.log_directory)
        except OSError:
            print ('Error: Creating directory. ' +  self.log_directory)

        file_name = self.log_directory + "/output_" + self.current_date.strftime("D%Y-%m-%d_") + self.current_date.strftime("T%H-%M-%S") + "_.txt"
        file = open(file_name, "w")
        file.write("defaultQuery = " + str(self.defaultQuery) + '\n\n')

        if self.defaultQuery is False:
            file.write("Accessing Sumo Search Query in: " + str(sys.argv[1]) + '\n\n')
        else:
            file.write("Accessing Sumo Search Query in: default_query.py" + '\n\n')

        file.write("Query:\n" + self.query + '\n\n')
        file.write("From " + self.fromTime + " To " + self.toTime + '\n\n')
        file.write("Query Results:\n")
        file.write(json.dumps(query_results) + '\n\n')
        file.write("FAILED SEARCH" + '\n\n')
        file.write("EXCEPTION:\n" + str(exception) + '\n\n')

        file.close()

        sys.exit("Status Code 1\nFailed Search")

    def get_ip_list(self,query_results):
        """
        Parses through query_results for dictionaries and then scans for "src_ip" keys appending to a list
        Input:
            query_results (List) : List of dictionaries containing the results of the SumoLogic query
        Return:
            ip_list (List)       : List of ip addresses to send to abuseIPDB for lookup
        """
        ip_list = []
        for dictionary in query_results:
            for key, value in dictionary.items():
                if key == "src_ip":
                    ip_list.append(value)

        try:
            ip_list[0]
        except IndexError as e:
            self.failed_search(e,query_results,console_show_join=True)

        return ip_list

    @staticmethod
    def join(ip_records,query_results):
        """
        Takes list of SumoLogic dictionaries and joins them with the list of dictionaries from abuseIPDB's
        results based on ip lookup
        Input:
            ip_record (List)      : List of dictionaries containing abuseIPDB's ip lookups
            query_results (List)  : List of dictionaries containing the results of the SumoLogic query
        Return:
            joined_results (List) : List of dictionaries, the join between ip_record and query_results
        """
        joined_results = []
        for record, dictionary in zip(ip_records, query_results):
            record = record.getAttributes(includeIP=False)
            temp = {}
            for key, value in record.items():
                temp[key + " (abuseIPDB)"] = value
            join = {**dictionary, **temp}
            joined_results.append(join)
        return joined_results

    def get_query_results(self):
        """
        Runs query through SumoLogic to get results of query
        Input:
            sumo_api (Class)         : 'sumologic.sumologic.SumoLogic', Sumo Logic Python SDK, https://github.com/SumoLogic/sumologic-python-sdk
        Return:
            query_results (List)     : List of dictionaries containing the results of the SumoLogic query
        """
        if self.defaultQuery is False:
            print("Accessing Sumo Search Query in: " + str(sys.argv[1]) + '\n')
            print("Query:\n" + self.query)
            print("From " + self.fromTime + " To " + self.toTime + '\n')
            query_results = self.sumo_api.search(self.query,fromTime=self.fromTime,toTime=self.toTime,timeZone=self.timeZone)
        else:
            print("Accessing Default Query in default_query.py\n")
            print("Query:\n" + self.query + '\n')
            print("From " + self.fromTime + " To " + self.toTime + '\n')
            try:
                query_results = self.sumo_api.search(self.query,fromTime=self.fromTime,toTime=self.toTime,timeZone=self.timeZone)
            except Exception as e:
                self.failed_search(e,query_results,console_show_join=True)
        print("Query Results: \n" + str(query_results) + '\n')
        return query_results

    def post_to_http_source(self,joined_results):
        """
        Posts joined_results to a collector in Sumo sumologic
        Input:
            joined_results (List)            : query_results with abuseIPDB results joined into each dictionary
        Return (None):
            Posts joined_results to specified selector
        """
        if self.postAuthorization is True:
            sumo_api_post = SumoLogic(self.sumo_access_id,self.sumo_access_key,endpoint="https://endpoint1.collection.us2.sumologic.com/receiver/v1/http/")
            post_object = sumo_api_post.post(self.uniqueHTTPCollectorCode,joined_results)
            print('\n')
            print(post_object)
        else:
            print("\nPost authorization disabled.\n")


def main():
    aggregator = SumoLogic_AbuseIPDB_Aggregator()

    query_results = aggregator.get_query_results()

    ipAddresses = aggregator.get_ip_list(query_results)

    ip_records = aggregator.abuseIPDB_lookup(ipAddresses)

    joined_results = aggregator.join(ip_records, query_results)

    aggregator.record_search(query_results,joined_results,console_show_join=True,return_fileName=False)

    aggregator.post_to_http_source(joined_results)

if __name__ == '__main__':
    main()
