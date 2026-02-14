import whois
from datetime import datetime
import socket

#Deals with error
stats = {
    "dns_fail": 0,
    "ssl_fail": 0,
    "whois_fail": 0
}


def domain_age(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date

        if creation is None:
            return -1         # no creation date → suspicious

        if isinstance(creation, list):
            creation = creation[0]

        age_days = (datetime.now() - creation).days
        return 1 if age_days > 365 else -1

    except whois.parser.PywhoisError:
        return -1             # domain info invalid → phishing
    except Exception:
        return 0              # firewall / timeout → unknown
    
    



dns_cache = {}

def dns_record(domain):
    try:
        socket.gethostbyname(domain)
        return 1              # resolves → legit signal
    except socket.gaierror:
        return -1             # domain does not exist → phishing
    except Exception:
        return 0              # other issues (firewall, OS) → unknown
    

def domain_registration_length(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date
        expiry = w.expiration_date

        if creation is None or expiry is None:
            return -1

        if isinstance(creation, list):
            creation = creation[0]
        if isinstance(expiry, list):
            expiry = expiry[0]

        length_days = (expiry - creation).days
        return 1 if length_days > 365 else -1

    except whois.parser.PywhoisError:
        return -1
    except Exception:
        return 0
    

import ssl


def ssl_final_state(domain):
    try:
        context = ssl.create_default_context()
        sock = socket.create_connection((domain, 443), timeout=3)
        with context.wrap_socket(sock, server_hostname=domain):
            return 1           # valid SSL
    except ssl.SSLError:
        return -1              # invalid certificate → phishing
    except socket.timeout:
        return 0               # firewall / blocked
    except Exception:
        return 0