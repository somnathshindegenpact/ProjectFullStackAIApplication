import importlib.util
import os
import sys

ROOT_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

BACKEND_APP_PATH = os.path.join(BACKEND_DIR, "app.py")
spec = importlib.util.spec_from_file_location("backend_app_module", BACKEND_APP_PATH)
backend_app = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = backend_app
spec.loader.exec_module(backend_app)

# Re-export the Flask app and supporting objects that backend modules import
# via `from app import ...`.
db = backend_app.db
migrate = backend_app.migrate
jwt = backend_app.jwt


def create_app():
    return backend_app.create_app()


app = create_app()
application = app
