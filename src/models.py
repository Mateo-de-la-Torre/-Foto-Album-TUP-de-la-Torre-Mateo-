from . import db

class Photo(db.Model):
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String, nullable=False)  # Aquí puedes almacenar la imagen en formato base64 o como un enlace

    def __repr__(self):
        return f'<Photo {self.title}>'