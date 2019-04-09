class IP_Profile:
    def __init__(self, score=None, country_code=None, country_name=None,
                 domain=None, ip_address=None, ip_version=None, is_public=None,
                 is_whitelisted=None, isp=None, last_report=None, usage_type=None,
                 reports=None, showReports=False):
        self.score = score
        self.country_code = country_code
        self.country_name = country_name
        self.domain = domain
        self.ip_address = ip_address
        self.ip_version = ip_version
        self.is_public = is_public
        self.is_whitelisted = is_whitelisted
        self.isp = isp
        self.last_report = last_report
        self.usage_type = usage_type
        self.reports = reports
        self.showReports = showReports

    def getAttributes(self, includeIP=False):
        if includeIP == True:
            return {
                "ipAddress": self.ip_address,
                "abuseConfidenceScore": self.score,
                "countryCode": self.country_code,
                "countryName": self.country_name,
                "domain": self.domain,
                "ipVersion": self.ip_version,
                "isPublic": self.is_public,
                "isWhitelisted": self.is_whitelisted,
                "isp": self.isp,
                "lastReportedAt": self.last_report,
                "usageType": self.usage_type,
                "reports": self.reports
            }
        else:
            return {
                "abuseConfidenceScore": self.score,
                "countryCode": self.country_code,
                "countryName": self.country_name,
                "domain": self.domain,
                "ipVersion": self.ip_version,
                "isPublic": self.is_public,
                "isWhitelisted": self.is_whitelisted,
                "isp": self.isp,
                "lastReportedAt": self.last_report,
                "usageType": self.usage_type,
                "reports": self.reports
            }

    def __str__(self):
        output = [
            self.ip_address,
            "\n\tabuseConfidenceScore: " + self.score,
            "\n\tcountryCode: " + self.country_code,
            "\n\tcountryName: " + self.country_name,
            "\n\tdomain: " + self.domain,
            "\n\tipVersion: " + self.ip_version,
            "\n\tisPublic: " + self.is_public,
            "\n\tisWhitelisted: " + self.is_whitelisted,
            "\n\tisp: " + self.isp,
            "\n\tlastReportedAt: " + self.last_report,
            "\n\tusageType: " + self.usage_type + '\n'
        ]
        if self.showReports == True:
            output.append("\treports: " + self.reports + '\n')
        return ''.join(output)
