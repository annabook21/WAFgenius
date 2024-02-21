# WAFgenius

The WAFgenius provides detailed insights into web traffic and security threats by analyzing AWS WAF logs. It includes features for basic metrics calculation, rule trigger analysis, and GeoIP analysis to identify the geographic locations of source IP addresses.

## Features

- **Basic Metrics Calculation**: Analyzes total requests, and categorizes them into allowed and blocked requests.
- **Rule Trigger Analysis**: Identifies which AWS WAF rules are triggered most frequently.
- **GeoIP Analysis**: Enriches log data with the geographic location of source IP addresses using the GeoLite2 database.

## Prerequisites

- Python 3.x
- Pandas library
- GeoIP2 library
- GeoLite2 City database (for GeoIP analysis)

## Installation

1. **Install Python 3.x**: Ensure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install Required Python Libraries**:

```bash
pip install pandas geoip2