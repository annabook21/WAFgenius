# WAFgenius

The WAFgenius provides detailed insights into web traffic and security threats by analyzing AWS WAF logs. It includes features for basic metrics calculation, rule trigger analysis, and GeoIP analysis to identify the geographic locations of source IP addresses.

## Features

- **Basic Metrics Calculation**: Analyzes total requests, and categorizes them into allowed and blocked requests.
- **Rule Trigger Analysis**: Identifies which AWS WAF rules are triggered most frequently.
- **GeoIP Analysis**: Enriches log data with the geographic location of source IP addresses using the GeoLite2 database.

## Prerequisites

- **Python**: Version 3.x
- **Pandas**: Used for data manipulation and analysis.
  - Installation: `pip install pandas`
- **GeoIP2**: Used for geolocation lookup.
  - Installation: `pip install geoip2`
- **Tkinter**: Used for creating the graphical user interface (GUI).
  - Installation: Included in the standard Python distribution.

  Additionally, you need the GeoLite2-City.mmdb file for geolocation lookup. You can download it from [MaxMind](https://dev.maxmind.com/geoip/geoip2/geolite2/) and place it in the same directory as the application.

## Installation

1. **Install Python 3.x**: Ensure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install Required Python Libraries**:

```bash
pip install pandas geoip2
```

## Usage

1. Clone or download the repository to your local machine.
2. Navigate to the project directory.
3. Ensure that you have Python and the required packages installed.
4. Download the GeoLite2-City.mmdb file from MaxMind and place it in the same directory as the application.
5. Replace `'path/to/your/logfile.json'` in the `main()` function with the path to your log file.
6. Run the `main()` function to analyze the log file.

### Running the GUI
- Alternatively, you can run the GUI interface by executing the script. The GUI allows you to select a log file using a file dialog and analyze it with a click of a button.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Anna Booker - https://www.linkedin.com/in/annadbooker

Project Link: [https://github.com/annabook21/WAFgenius](https://github.com/annabook21/WAFgenius)

