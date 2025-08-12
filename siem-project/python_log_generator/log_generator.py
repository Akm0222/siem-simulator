import time
import datetime
import random
from faker import Faker
from elasticsearch import Elasticsearch

# --- NEW: Connect directly to Elasticsearch ---
try:
    es = Elasticsearch("http://localhost:9200")
    print("Successfully connected to Elasticsearch")
except Exception as e:
    print(f"Could not connect to Elasticsearch: {e}")
    exit()

fake = Faker()

log_types = {
    "apache_access": lambda: {
        "message": f'{fake.ipv4(network=False)} - - [{datetime.datetime.now().strftime("%d/%b/%Y:%H:%M:%S %z")}] "GET /{fake.uri_path()} HTTP/1.1" {random.choice([200, 404, 500])} {random.randint(200, 5000)}',
        "event_type": "apache_access",
        "source_ip": fake.ipv4(network=False)
    },
    "ssh_failed": lambda: {
        "message": f'{datetime.datetime.now().strftime("%b %d %H:%M:%S")} server sshd[1234]: Failed password for invalid user {fake.user_name()} from {fake.ipv4(network=False)} port 22 ssh2',
        "event_type": "ssh_auth",
        "tags": ["threat_detected", "failed_login"],
        "threat_level": "medium",
        "source_ip": fake.ipv4(network=False)
    },
    "firewall_drop": lambda: {
        "message": f'{datetime.datetime.now().strftime("%b %d %H:%M:%S")} kernel: [UFW BLOCK] IN=eth0 OUT= MAC=... SRC={fake.ipv4(network=False)} DST={fake.ipv4(network=False)} PROTO=TCP DPT=23',
        "event_type": "firewall",
        "tags": ["threat_detected", "firewall_drop"],
        "threat_level": "high",
        "source_ip": fake.ipv4(network=False)
    }
}

def generate_log_line():
    log_type_key = random.choices(list(log_types.keys()), weights=[10, 3, 4], k=1)[0]
    log_data = log_types[log_type_key]()
    
    log_data["@timestamp"] = datetime.datetime.utcnow()
    return log_data

print("Log generator started. Sending logs directly to Elasticsearch.")
print("Press Ctrl+C to stop.")

try:
    while True:
        log_entry = generate_log_line()
        try:
            es.index(index=f"siem-logs-{datetime.datetime.now().strftime('%Y.%m.%d')}", document=log_entry)
            print(f"Log sent: {log_entry['message']}")
        except Exception as e:
            print(f"Failed to send log to Elasticsearch: {e}")

        time.sleep(random.uniform(0.5, 2.0))
except KeyboardInterrupt:
    print("\nLog generator stopped.")