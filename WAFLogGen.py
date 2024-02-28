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
    "90.188.0.0", "91.76.0.0", "91.105.128.0", # ... and so on with the rest of the IPs
    # Add all the IP addresses you provided here
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
with open('/mnt/data/ddos_log.json', 'w') as f:
    json.dump(log_entries, f, indent=2)

print(f"Generated {len(log_entries)} log entries.")
