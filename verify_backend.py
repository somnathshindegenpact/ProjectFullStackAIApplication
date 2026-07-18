import importlib.util
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

BACKEND_APP_PATH = os.path.join(BACKEND_DIR, 'app.py')
spec = importlib.util.spec_from_file_location('backend_app_module', BACKEND_APP_PATH)
backend_app = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = backend_app
spec.loader.exec_module(backend_app)
print('imported', hasattr(backend_app, 'application'))
flask_app = backend_app.application
print('routes_ok', '/api/health' in [str(rule) for rule in flask_app.url_map.iter_rules()])
with flask_app.test_client() as client:
    resp = client.get('/api/health')
    print(resp.status_code)
    print(resp.get_data(as_text=True))
