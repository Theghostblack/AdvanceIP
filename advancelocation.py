#!/usr/bin/env python3
"""
ipinfo_lookup.py

Query https://ipinfo.io/<IP>/json and display all available information.

Usage:
    python ipinfo_lookup.py 8.8.8.8
    python ipinfo_lookup.py          # prompts for IP or hostname

Optional:
    Set environment variable IPINFO_TOKEN to use a token:
      export IPINFO_TOKEN="your_token_here"
"""

import os
import sys
import argparse
import requests
import json
import pyfiglet
import time

API_BASE = "https://ipinfo.io"

os.system("cls" if os.name == "nt" else "clear")


banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⣯⣭⣽⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣽⣿⣿⣿⣿⣟⣿⣿⣿⣿⣟⢿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠉⠻⣿⣿⣿⣿⣿⣿⣟⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠘⣿⣷⢻⣿⣿⣿⡽⣿⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡏⣿⣿⣿⣿⣿⡟⠀⢀⣀⡀⠀⠘⣿⡟⣿⣿⣼⣿⣻⣛⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡿⢠⣶⣿⣿⣿⣿⡄⢹⣿⣿⣿⣿⣿⣿⣷⣿⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣻⣿⣿⣿⣿⣿⣿⡇⣻⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣾⣿⣿⡇⠹⣿⣿⣿⣿⣿⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠈⠙⠛⠋⠁⠀⣾⣿⣿⣿⢫⣿⣿⣿⢹⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⣿⣿⣿⣽⣿⣿⣿⣿⣷⡀⠀⢀⣾⣿⣿⣿⣿⣿⣷⣯⣿⣿⣎⣿⣯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣷⣤⣿⣿⣿⣿⣿⣿⣿⣿⡧⣿⢻⣾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣏⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣁⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣧⣿⣟⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡿⠏⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠈⠻⣿⣾⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣻⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⢿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣷⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
.::.:::::::       .::.:::     .::.::::::::    .::::
.::.::    .::     .::.: .::   .::.::        .::    .::
.::.::    .::     .::.:: .::  .::.::      .::        .::
.::.:::::::       .::.::  .:: .::.::::::  .::        .::
.::.::            .::.::   .: .::.::      .::        .::
.::.::            .::.::    .: ::.::        .::     .::
.::.::            .::.::      .::.::          .::::

"""
print(banner)
time.sleep(2)  # waits 2 seconds

# Step 2: Print the rest of your program
print("Welcome to My Tool!")
print("Initializing...")
time.sleep(1)
print("Setup complete. Ready to go!")

banner= '''
@@@@created by theghostblack '''
print(banner)

def get_ip_info(target: str, token: str | None = None, timeout: float = 10.0) -> dict:
    """Query ipinfo.io for the given target (IP or hostname)."""
    url = f"{API_BASE}/{target}/json"
    headers = {"User-Agent": "ipinfo-lookup-script/1.0"}
    params = {}
    if token:
        params["token"] = token
    resp = requests.get(url, headers=headers, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def pretty_print_info(info: dict):
    """Nicely print the JSON info and derive some helpful fields."""
    # Print raw JSON pretty
    print("\n--- raw JSON from ipinfo.io ---")
    print(json.dumps(info, indent=2, ensure_ascii=False))
    print("\n--- parsed fields ---")

    # Common fields ipinfo provides
    fields = ["ip", "hostname", "city", "region", "country", "loc", "org", "postal", "timezone", "readme"]
    for f in fields:
        if f in info:
            print(f"{f:9}: {info[f]}")

    # Break out loc into latitude/longitude and provide a Google Maps link
    loc = info.get("loc")
    if loc:
        try:
            lat_str, lon_str = loc.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            print(f"latitude : {lat}")
            print(f"longitude: {lon}")
            print(f"maps link: https://www.google.com/maps/search/?api=1&query={lat},{lon}")
        except Exception:
            # If parsing fails just print loc as-is
            print(f"loc      : {loc}")

    # If there are other fields, print them
    extras = {k: v for k, v in info.items() if k not in fields}
    if extras:
        print("\n--- other fields returned ---")
        for k, v in extras.items():
            print(f"{k:9}: {v}")

def main():
    parser = argparse.ArgumentParser(description="Lookup IP details from ipinfo.io")
    parser.add_argument("target", nargs="?", help="IP address or hostname to lookup (default: prompts you)")
    parser.add_argument("--token", "-t", help="IPInfo API token (optional). You can also set IPINFO_TOKEN env var")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    args = parser.parse_args()

    target = args.target
    if not target:
        target = input("Enter IP address or hostname (leave blank for your own IP): ").strip() or ""

    token = args.token or os.environ.get("IPINFO_TOKEN")

    try:
        info = get_ip_info(target, token=token, timeout=args.timeout)
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        body = e.response.text if e.response is not None else ""
        print(f"HTTP error querying ipinfo.io (status {status}).")
        if body:
            print("Response body:", body)
        sys.exit(1)
    except requests.RequestException as e:
        print("Network error:", str(e))
        sys.exit(1)

    pretty_print_info(info)

if __name__ == "__main__":
    main()
