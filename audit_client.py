"""
Oikonomia Public Synthetic Audit Client
Validates remote HTTP and socket latency against a running AWS F2 appliance.
Supports direct IP/port addressing or encrypted production endpoints.
"""
import sys
import time
import json
import requests

def audit_remote_endpoint(target_host, port=8000, secure=False):
    if target_host.startswith("http://") or target_host.startswith("https://"):
        base_url = target_host.rstrip("/")
    else:
        scheme = "https" if secure or port == 443 else "http"
        port_str = "" if (scheme == "https" and port == 443) or (scheme == "http" and port == 80) else f":{port}"
        base_url = f"{scheme}://{target_host}{port_str}"

    url = f"{base_url}/risk/evaluate"
    payload = {
        "sequence_data": [101, 2054, 2003, 1037, 3899],
        "target_motif": [1037]
    }
    headers = {"Content-Type": "application/json"}

    print(f"[*] Dispatching pre-flight audit packet to: {url}")
    
    try:
        t0 = time.perf_counter()
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        t1 = time.perf_counter()

        round_trip_ms = (t1 - t0) * 1000.0
        print(f"[+] HTTP Status Code : {resp.status_code}")
        print(f"[+] WAN Round-Trip   : {round_trip_ms:.3f} ms")
        
        if resp.status_code == 200:
            print("[+] Appliance Hardware Telemetry:")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"[-] Preemption / Rejection Response:\n{resp.text}")

    except requests.exceptions.ConnectionError:
        print(f"[!] FATAL: Connection refused at {url}.")
        print("[!] Ensure the target appliance is started and port is open in Security Groups.")
    except requests.exceptions.Timeout:
        print(f"[!] FATAL: Request timed out connecting to {url}.")
    except Exception as e:
        print(f"[!] Execution Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Direct IP/VPC : python audit_client.py <INSTANCE_IP> [PORT]")
        print("  Production URL: python audit_client.py eval.oikonomia-platform.com 443 --secure")
        sys.exit(1)

    host = sys.argv[1]
    target_port = 8000
    is_secure = False

    if len(sys.argv) >= 3:
        try:
            target_port = int(sys.argv[2])
        except ValueError:
            if sys.argv[2] == "--secure":
                is_secure = True

    if "--secure" in sys.argv:
        is_secure = True

    audit_remote_endpoint(host, port=target_port, secure=is_secure)
