import urllib.request
req = urllib.request.Request('https://task-manager-api-346f.onrender.com/api/auth/login', method='OPTIONS')
req.add_header('Origin', 'https://somnathshindegenpact.github.io')
req.add_header('Access-Control-Request-Method', 'POST')
req.add_header('Access-Control-Request-Headers', 'Content-Type,Authorization')
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        print('status', resp.status)
        for k, v in resp.headers.items():
            print(k, '=', v)
except Exception as e:
    print('error', repr(e))
