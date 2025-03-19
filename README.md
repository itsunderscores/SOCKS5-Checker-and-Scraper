# SOCKS5 Proxy Checker

A Python-based SOCKS5 proxy checker that scrapes proxy addresses from various sources and tests them for validity. It allows you to adjust the number of threads used during the check for faster processing.

## Requirements

Before running this script, ensure you have the following dependencies installed:

- Python 3.6+  
- `requests`  
- `beautifulsoup4`  
- `threading`

You can install the required packages using:

```bash
pip install requests beautifulsoup4
pip install requests
pip install pysocks
```

## Usage
Clone the repository:
```bash
git clone https://github.com/itsunderscores/SOCKS5-Checker-and-Scraper.git
```

Navigate into the project folder:
```bash
cd socks5-proxy-checker
```

Run the script:
```bash
python main.py
```

## Adjusting Threads
The script will scrape proxy addresses from various sources and check their SOCKS5 validity.
By default, the script uses 1000 threads to check proxies. You can adjust the number of threads by modifying the following line in `main.py`:

```bash
semaphore = threading.Semaphore(1000)  # Adjust as needed
```

Change the 1000 to the desired number of threads. Be mindful that using too many threads can affect the performance of your system, so adjust according to your needs.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
