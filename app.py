from src import crear_app, db
from src.models import Photo

app = crear_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
