import socks
import socket
import concurrent.futures
import threading
import signal
import sys
import time
import json
import urllib.request
import requests
from datetime import datetime
from scraper import list1, logtofile, remove_duplicate_proxies

# Semaphore to control the number of concurrent threads
semaphore = threading.Semaphore(1000)  # Adjust as needed

# Flag to indicate if CTRL+C is pressed
stop_threads = False

# URL to fetch JSON data
json_url = 'http://ip-api.com/json/'
url_request_timeout = 5

# List to hold valid proxies
valid_proxies = []

def signal_handler(sig, frame):
    global stop_threads
    print('\nYou pressed Ctrl+C! Stopping threads...')
    stop_threads = True

def print_progress_bar(processed, total, bar_length=30):
    progress = processed / total
    arrow = '=' * int(round(progress * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    percent = round(progress * 100)
    sys.stdout.write(f"\r[{arrow}{spaces}] {processed}/{total} ({percent}%)")
    sys.stdout.flush()

def check_socks5_proxy(ip, port, total_proxies, processed_proxies):
    socks.setdefaultproxy(socks.SOCKS5, ip, port, True)
    socket.socket = socks.socksocket

    try:
        while not stop_threads:  # Check for stop condition regularly
            start_time = time.time()
            response = urllib.request.urlopen(json_url, timeout=url_request_timeout)
            json_data = json.loads(response.read().decode())
            elapsed_time = round(time.time() - start_time, 2)

            city = json_data.get('city', 'Unknown')
            state = json_data.get('regionName', 'Unknown')
            country = json_data.get('countryCode', 'Unknown')
            isp = json_data.get('isp', 'Unknown')

            valid_proxies.append(f"{ip}:{port}")
            break  # Proxy checked successfully, break out of the loop
    except Exception:
        pass  # Silently ignore failed proxies
    finally:
        processed_proxies[0] += 1
        print_progress_bar(processed_proxies[0], total_proxies)
        semaphore.release()

def is_valid_proxy_format(proxy):
    return len(proxy) == 2 and proxy[0] and proxy[1].isdigit()

def save_proxies_to_file(output_file):
    with open(output_file, "w") as f:
        f.write("\n".join(valid_proxies) + "\n")
    print(f"\nSuccessfully saved {len(valid_proxies)} valid proxies to {output_file}.")

def scrape():
    print("Scraping Proxies...")
    try:
        os.remove("proxies.txt") 
        os.remove("unique_proxies.txt")
    except:
        pass

    for x in list1:
        blah = requests.get(url=x)
        logtofile("proxies.txt", blah.text)
        #print(blah.text)
    print("Finished scraping!")
    remove_duplicate_proxies('proxies.txt', 'unique_proxies.txt')
    os.remove("proxies.txt") 

def main():
    scrape()

    input_file = "unique_proxies.txt"
    output_file = "working_socks5.txt"
    signal.signal(signal.SIGINT, signal_handler)

    # Read proxies from the input file
    with open(input_file, "r") as f:
        proxies = [line.strip().split(":") for line in f if ":" in line.strip()]

    total_proxies = len(proxies)
    processed_proxies = [0]  # Shared list to track processed proxies

    print(f"Total proxies to check: {total_proxies}")
    print("Starting to check proxies...\n")

    # Use ThreadPoolExecutor to check proxies concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = [executor.submit(check_socks5_proxy, ip, int(port), total_proxies, processed_proxies)
                   for ip, port in proxies if is_valid_proxy_format((ip, port))]

        # Wait for all futures to complete or for Ctrl+C
        for future in concurrent.futures.as_completed(futures):
            if stop_threads:
                break
            future.result()

    # Save the valid proxies to file
    save_proxies_to_file(output_file)

    print("\nFinished checking proxies.")

if __name__ == "__main__":
    main()
