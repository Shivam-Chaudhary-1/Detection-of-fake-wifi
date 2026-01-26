import requests
import time

URL = 'http://localhost:8000/predict'

payload = {
    'agent_id': 'test_agent',
    'timestamp': time.time(),
    'scans': [
        {'ssid': 'Home-1', 'bssid': 'aa:bb:cc:dd:ee:ff', 'signal': -40, 'channel': 6, 'security': 'WPA2', 'vendor': 'TP-Link'},
        {'ssid': 'Guest_Free', 'bssid': '11:22:33:44:55:66', 'signal': -45, 'channel': 11, 'security': 'OPEN', 'vendor': 'None'}
    ]
}

resp = requests.post(URL, json=payload, timeout=5)
print(resp.status_code)
print(resp.json())
