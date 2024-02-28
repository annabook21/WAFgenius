import json
import random
from datetime import datetime, timedelta

# Base log entry from which to create the other entries
base_log_entry = {
    "timestamp": 1702556780000,
    "formatVersion": 1,
    "webaclId": "arn:aws:wafv2:us-east-1:123456789012:global/webacl/my-webacl-name/12345678-90ab-cdef-1234-567890abcdef",
    "terminatingRuleId": "Custom_Rule_Block",
    "terminatingRuleType": "REGULAR",
    "action": "BLOCK",
    "terminatingRuleMatchDetails": [],
    "httpSourceName": "ALB",
    "httpSourceId": "E2JK6G7H8I9J0K",
    "ruleGroupList": [
        # ... your rule groups here ...
    ],
    "rateBasedRuleList": [],
    "nonTerminatingMatchingRules": [],
    "requestHeadersInserted": None,
    "responseCodeSent": None,
    "httpRequest": {
        "clientIp": "89.237.63.255",
        "country": "RU",
        "headers": [
            # ... your headers here ...
        ],
        "uri": "/path/to/resource",
        "args": "query=parameters",
        "httpVersion": "HTTP/1.1",
        "httpMethod": "GET",
        "requestId": "abcdef123456-7890-abcd-ef12-34567890abcd"
    },
    "labels": [],
    "requestBodySize": 532,
    "requestBodySizeInspectedByWAF": 532,
    "ja3Fingerprint": "d8e8fca2dc0f896fd7cb4cb0031ba249"
}

# IPs to simulate the attacks from
ips = [
    "90.188.0.0", 
    "91.76.0.0", 
    "91.105.128.0", 
    "91.107.0.0", 
    "91.109.64.0", 
    "91.109.128.0", 
    "91.122.0.0", 
    "91.123.16.0", 
    "91.123.80.0", 
    "91.133.0.0", 
    "91.135.144.0", 
    "217.170.112.0", 
    "217.170.208.0", 
    "217.171.0.0", 
    "217.173.16.0", 
    "217.173.64.0", 
    "217.174.0.0", 
    "217.174.96.0", 
    "217.175.0.0", 
    "217.175.16.0", 
    "217.175.32.0", 
    "217.175.128.0", 
    "217.175.144.0", 
    "217.194.240.0", 
    "217.195.64.0", 
    "217.195.80.0", 
    "31.134.128.0", 
    "31.134.224.0", 
    "31.135.32.0", 
    "31.135.64.0", 
    "31.135.96.0", 
    "31.135.224.0", 
    "31.162.0.0", 
    "31.172.192.0", 
    "31.173.0.0", 
    "31.177.64.0", 
    "31.180.0.0", 
    "31.184.208.0", 
    "31.186.64.0", 
    "31.186.128.0", 
    "31.192.128.0", 
    "31.192.160.0", 
    "31.200.192.0", 
    "31.200.224.0", 
    "31.204.0.0", 
    "31.204.96.0", 
    "31.204.160.0", 
    "31.207.64.0", 
    "31.207.128.0", 
    "31.210.192.0", 
    "31.211.0.0", 
    "31.216.160.0", 
    "31.220.160.0", 
    "37.1.0.0", 
    "37.1.64.0", 
    "37.1.128.0", 
    "37.8.144.0", 
    "37.9.0.0", 
    "37.9.64.0", 
    "37.9.144.0", 
    "37.19.32.0", 
    "37.20.0.0", 
    "37.28.160.0", 
    "37.29.0.0", 
    "37.49.160.0", 
    "37.49.192.0", 
    "37.60.208.0", 
    "37.72.64.0", 
    "37.76.128.0", 
    "37.78.0.0", 
    "37.98.160.0", 
    "37.98.240.0", 
    "37.110.0.0", 
    "37.110.128.0", 
    "37.110.224.0", 
    "37.112.0.0", 
    "37.114.16.0", 
    "37.122.0.0", 
    "37.131.192.0", 
    "37.139.96.0", 
    "37.139.192.0", 
    "37.140.0.0", 
    "37.140.128.0", 
    "37.143.16.0", 
    "37.143.96.0", 
    "37.144.0.0", 
    "37.153.0.0", 
    "37.188.0.0", 
    "37.190.0.0", 
    "37.192.0.0"
]

# List to hold all the log entries
log_entries = []

# Current time for the log entries
current_time = datetime.now()

# Generate a log entry for each IP
for ip in ips:
    # Create a new log entry by copying the base entry
    new_entry = json.loads(json.dumps(base_log_entry))
    
    # Modify the necessary fields
    new_entry['httpRequest']['clientIp'] = ip
    new_entry['timestamp'] = int(current_time.timestamp() * 1000)
    
    # Append the new entry to the list of log entries
    log_entries.append(new_entry)
    
    # Increment the current time slightly for the next entry to simulate an ongoing attack
    current_time += timedelta(seconds=random.randint(1, 10))

# Save the log entries to a file
with open('C:\Users\asiabook\Desktop\Python\WAFgenius/ddos_log.json', 'w') as f:
    json.dump(log_entries, f, indent=2)

print(f"Generated {len(log_entries)} log entries.")
