from api.app.main import app

def test_app_instance():
    assert app.title == "Projeto Futuro V1 API"
