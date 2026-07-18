import httpx
import json

url = 'http://127.0.0.1:5000/api/auth/login'
payload = {'email':'demo@example.com','password':'password'}
resp = httpx.post(url, json=payload)
print(resp.status_code)
try:
    print(json.dumps(resp.json(), indent=2))
except Exception:
    print(resp.text)
