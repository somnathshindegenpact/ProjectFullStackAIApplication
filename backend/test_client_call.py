from app import create_app
app = create_app()

with app.test_client() as c:
    resp = c.post('/api/auth/login', json={'email':'demo@example.com','password':'password'})
    print('status', resp.status_code)
    print(resp.get_data(as_text=True))
