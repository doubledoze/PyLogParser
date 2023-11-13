import socket
import re
import sys
from datetime import datetime
import geoip2.database


def parse_line(line):
    # Extraction des informations de chaque ligne, en ajustant pour IPv4 et IPv6
    match = re.search(r'(\S+) \[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) \+\d{4}\]', line)
    ip, timestamp = match.groups()

    # Retirer ::ffff: uniquement si en début d'adresse
    if ip.startswith('::ffff:'):
        ip = ip.replace('::ffff:', '')

    return ip, timestamp

def nslookup(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return "Reverse DNS not found"

def geoip_lookup(ip):
    with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:
        try:
            response = reader.city(ip)
            return f"{response.city.name}, {response.country.name}"
        except geoip2.errors.AddressNotFoundError:
            return "Location not found"

def filter_log(start_time, end_time, filepath):
    start_datetime = datetime.strptime(start_time, "%d/%b/%Y:%H:%M:%S")
    end_datetime = datetime.strptime(end_time, "%d/%b/%Y:%H:%M:%S")
    processed_ips = set()  # Ensemble pour stocker les IPs déjà traitées

    with open(filepath, 'r') as file:
        for line in file:
            ip, timestamp = parse_line(line)
            current_datetime = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S")

            if start_datetime <= current_datetime <= end_datetime:
                if ip not in processed_ips:
                    processed_ips.add(ip)
                    reverse_dns = nslookup(ip)
                    geoip = geoip_lookup(ip)
                    print(f"IP: {ip}, Timestamp: {timestamp}, Reverse DNS: {reverse_dns}, GeoIP: {geoip}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 parser.py [start_time] [end_time] [logfile_path]")
        sys.exit(1)

    start_time = sys.argv[1]
    end_time = sys.argv[2]
    logfile_path = sys.argv[3]

    filter_log(start_time, end_time, logfile_path)
