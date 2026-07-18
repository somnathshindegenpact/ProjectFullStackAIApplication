import httpx, json
url = 'http://127.0.0.1:5000/api/auth/register'
payload = {'email':'tmpuser@example.com','password':'pw123'}
resp = httpx.post(url, json=payload)
print(resp.status_code)
print(resp.text)
