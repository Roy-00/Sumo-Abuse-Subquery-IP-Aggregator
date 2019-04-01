import subprocess
import json
from ip_profile import IP_Profile

class AbuseIPDB:
    category_codes = {          #implement if examining report categories
        '3': 'Frad_Orders',
        '4': 'DDoS_Attack',
        '5': 'FTP_Brute-Force',
        '6': 'Ping of Death',
        '7': 'Phishing',
        '8': 'Fraud VoIP',
        '9': 'Open_Proxy',
        '10': 'Web_Spam',
        '11': 'Email_Spam',
        '12': 'Blog_Spam',
        '13': 'VPN IP',
        '14': 'Port_Scan',
        '15': 'Hacking',
        '16': 'SQL Injection',
        '17': 'Spoofing',
        '18': 'Brute_Force',
        '19': 'Bad_Web_Bot',
        '20': 'Exploited_Host',
        '21': 'Web_App_Attack',
        '22': 'SSH',
        '23': 'IoT_Targeted'
    }

    @staticmethod
    def check_ip(ipAddress, days, my_apiV2_key):
        command = 'curl -G https://api.abuseipdb.com/api/v2/check --data-urlencode "ipAddress=' + ipAddress + '" -d maxAgeInDays=' + days + ' -d verbose -H "Key: ' + my_apiV2_key + '" -H "Accept: application/json"'
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        json_load = json.loads(output)
        return json_load

    @staticmethod
    def record_ip_data(json_load, include_reports=False, indent=False):
        checklist = [
                     "abuseConfidenceScore", "countryCode", "countryName",
                     "domain", "ipAddress", "ipVersion", "isPublic",
                     "isWhitelisted", "isp", "lastReportedAt", "usageType"
                    ]
        if include_reports == True:
            checklist.append("reports")
        retrieved = []
        for item in checklist:
            if indent == True:
                retrieved.append(str(json.dumps(json_load["data"][item], indent=3, sort_keys=True)))
            else:
                retrieved.append(str(json_load["data"][item]))
        if include_reports == True:
            ip_data = IP_Profile(*retrieved, showReports=True)
        else:
            ip_data = IP_Profile(*retrieved)
        return ip_data
