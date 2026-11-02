"""
Oikonomia Public Synthetic Audit Client
Validates remote HTTP and socket latency against a running AWS F2 appliance.
"""
import time
import requests
import json

def audit_remote_endpoint(host_ip, port=8000):
    url = f"http://{host_ip}:{port}/risk/evaluate"
    payload = {"sequence_data": [1, 0, 1, 1], "target_motif": [1]}
    headers = {"Content-Type": "application/json"}
    
    print(f"[*] Dispatching test packet to {url}...")
    t0 = time.perf_counter()
    resp = requests.post(url, json=payload, headers=headers)
    t1 = time.perf_counter()
    
    round_trip_ms = (t1 - t0) * 1000.0
    print(f"[+] Status: {resp.status_code}")
    print(f"[+] Round-Trip Wall Clock: {round_trip_ms:.3f} ms")
    print(f"[+] Appliance Telemetry:\n{json.dumps(resp.json(), indent=2)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python audit_client.py <INSTANCE_PUBLIC_OR_VPC_IP>")
    else:
        audit_remote_endpoint(sys.argv[1])
